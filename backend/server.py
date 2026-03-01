#!/usr/bin/env python3
"""
Clouding Synthesizer — WebSocket backend
Multi-player room-based synthesizer server.
Broadcasts oscillator data at 10Hz + relays player state for battle mode.
"""

import asyncio
import json
import math
import random
import time
import uuid
from collections import deque

import numpy as np

try:
    import websockets
except ImportError:
    print("Install websockets: pip3 install websockets")
    raise

# ── Token simulation config ──────────────────────────────────────────────────

TOKENS = [
    {"name": "ETH",  "base": 3245.0,  "vol": 0.0008},
    {"name": "BTC",  "base": 67500.0, "vol": 0.0005},
    {"name": "SOL",  "base": 178.0,   "vol": 0.0015},
    {"name": "LINK", "base": 18.5,    "vol": 0.0012},
    {"name": "UNI",  "base": 12.3,    "vol": 0.0014},
    {"name": "AAVE", "base": 285.0,   "vol": 0.0010},
    {"name": "ARB",  "base": 1.85,    "vol": 0.0018},
    {"name": "OP",   "base": 3.42,    "vol": 0.0016},
]

TICK_HZ = 10
TICK_INTERVAL = 1.0 / TICK_HZ
FOURIER_WINDOW = 64
FOURIER_BINS = 32

# ── Lorenz attractor ─────────────────────────────────────────────────────────

SIGMA = 10.0
RHO = 28.0
BETA = 8.0 / 3.0
LORENZ_DT = 0.005


class LorenzState:
    def __init__(self):
        self.x = 1.0 + random.random()
        self.y = 1.0 + random.random()
        self.z = 1.0 + random.random()

    def step(self, perturbation=0.0):
        dx = SIGMA * (self.y - self.x) + perturbation * 0.1
        dy = self.x * (RHO - self.z) - self.y
        dz = self.x * self.y - BETA * self.z
        self.x += dx * LORENZ_DT
        self.y += dy * LORENZ_DT
        self.z += dz * LORENZ_DT
        return self.x, self.y, self.z


# ── Token state ───────────────────────────────────────────────────────────────

class TokenSim:
    def __init__(self, cfg):
        self.name = cfg["name"]
        self.price = cfg["base"] * (1.0 + random.uniform(-0.02, 0.02))
        self.volatility = cfg["vol"]
        self.delta = 0.0
        self.volume = 0.0
        self.delta_history = deque(maxlen=FOURIER_WINDOW)

    def tick(self):
        change = random.gauss(0, self.volatility)
        self.delta = change
        self.price *= (1.0 + change)
        self.price = max(self.price * 0.01, self.price)
        self.volume = max(0.0, random.expovariate(2.0) + abs(change) * 50.0)
        self.delta_history.append(self.delta)
        return {
            "name": self.name,
            "price": round(self.price, 4),
            "delta": round(self.delta, 6),
            "volume": round(self.volume, 4),
        }


# ── Oscillator engine ────────────────────────────────────────────────────────

class OscillatorEngine:
    def __init__(self, tokens):
        self.tokens = tokens
        self.lorenz = LorenzState()
        self.tick_count = 0
        self.t = 0.0

    def compute(self):
        self.tick_count += 1
        self.t += TICK_INTERVAL

        deltas = [t.delta for t in self.tokens]
        avg_delta = sum(deltas) / len(deltas)
        total_volume = sum(t.volume for t in self.tokens)
        max_abs_delta = max(abs(d) for d in deltas) if deltas else 0.0

        volatility_signal = avg_delta * 1000.0
        lx, ly, lz = self.lorenz.step(volatility_signal)

        s1 = math.sin(self.t * 0.3 * math.pi * 2 + avg_delta * 100)
        s2 = math.sin(self.t * 0.5 * math.pi * 2 + max_abs_delta * 200) * 0.6
        s3 = math.sin(self.t * 0.8 * math.pi * 2) * 0.3
        sine_mix = s1 + s2 + s3

        combined_deltas = []
        for t in self.tokens:
            combined_deltas.extend(t.delta_history)
        if len(combined_deltas) >= FOURIER_WINDOW:
            sample = np.array(combined_deltas[-FOURIER_WINDOW:])
            fft = np.abs(np.fft.rfft(sample))[:FOURIER_BINS]
            fft_max = fft.max() if fft.max() > 0 else 1.0
            fourier_bins = (fft / fft_max).tolist()
            dominant_freq = float(np.argmax(fft)) / FOURIER_BINS
        else:
            fourier_bins = [0.0] * FOURIER_BINS
            dominant_freq = 0.0

        w_raw = dominant_freq * 0.6 + (sine_mix * 0.5 + 0.5) * 0.4
        w = max(0.0, min(1.0, w_raw))
        amplitude = min(1.0, max_abs_delta * 500.0 + 0.2)
        phase = (self.t * 0.5) % 1.0
        tempo = 0.3 + min(0.5, total_volume * 0.02)
        block_number = 19000000 + int(self.t * 0.08)

        return {
            "oscillator": {
                "x": round(lx, 4), "y": round(ly, 4),
                "z": round(lz, 4), "w": round(w, 4),
            },
            "fourier": [round(f, 4) for f in fourier_bins],
            "block": {"number": block_number},
            "phase": round(phase, 4),
            "amplitude": round(amplitude, 4),
            "tempo": round(tempo, 4),
            "sine_mix": round(sine_mix, 4),
        }


# ── Multi-player room ────────────────────────────────────────────────────────

PLAYERS = {}  # ws -> {id, name, color, state}


def player_list():
    """Get serializable list of all players."""
    return [
        {"id": p["id"], "name": p["name"], "color": p["color"],
         "notes": p.get("notes", []), "fx": p.get("fx", {})}
        for p in PLAYERS.values()
    ]


COLORS = ["#ff6b6b", "#ffd93d", "#6bcb77", "#4d96ff",
          "#ff6fff", "#ff9f43", "#00d2d3", "#c792ea"]
color_idx = 0


async def handler(ws):
    global color_idx
    pid = str(uuid.uuid4())[:8]
    pcolor = COLORS[color_idx % len(COLORS)]
    color_idx += 1
    PLAYERS[ws] = {"id": pid, "name": f"Player-{pid[:4]}", "color": pcolor,
                   "notes": [], "fx": {}}
    count = len(PLAYERS)
    print(f"Player {pid} connected ({count} total)")

    # Send welcome with player ID
    await ws.send(json.dumps({"type": "welcome", "id": pid, "color": pcolor,
                               "players": player_list()}))
    # Notify others
    join_msg = json.dumps({"type": "player_join", "player": PLAYERS[ws],
                            "count": count})
    for c in list(PLAYERS.keys()):
        if c != ws:
            try:
                await c.send(join_msg)
            except Exception:
                pass

    try:
        async for raw in ws:
            try:
                msg = json.loads(raw)
            except json.JSONDecodeError:
                continue
            mt = msg.get("type", "")
            if mt == "state":
                # Player broadcasting their current state
                p = PLAYERS.get(ws)
                if p:
                    p["notes"] = msg.get("notes", [])
                    p["fx"] = msg.get("fx", {})
                    if "name" in msg:
                        p["name"] = msg["name"][:16]
                    # Relay to others
                    relay = json.dumps({"type": "player_state",
                                         "id": p["id"], "notes": p["notes"],
                                         "fx": p["fx"], "name": p["name"],
                                         "color": p["color"]})
                    for c in list(PLAYERS.keys()):
                        if c != ws:
                            try:
                                await c.send(relay)
                            except Exception:
                                pass
    finally:
        p = PLAYERS.pop(ws, None)
        count = len(PLAYERS)
        print(f"Player {pid} disconnected ({count} total)")
        leave_msg = json.dumps({"type": "player_leave", "id": pid,
                                 "count": count})
        for c in list(PLAYERS.keys()):
            try:
                await c.send(leave_msg)
            except Exception:
                pass


async def broadcast_loop(tokens, engine):
    while True:
        t0 = time.monotonic()
        token_data = [t.tick() for t in tokens]
        osc_data = engine.compute()

        payload = json.dumps({
            "type": "tick",
            "tokens": token_data,
            **osc_data,
            "players": player_list(),
            "timestamp": time.time(),
        })

        for c in list(PLAYERS.keys()):
            try:
                await c.send(payload)
            except Exception:
                pass

        elapsed = time.monotonic() - t0
        await asyncio.sleep(max(0, TICK_INTERVAL - elapsed))


async def main():
    tokens = [TokenSim(cfg) for cfg in TOKENS]
    engine = OscillatorEngine(tokens)

    print("Clouding Synthesizer backend starting on ws://0.0.0.0:8765")
    print("Multi-player battle mode enabled — all connections share the room")

    async with websockets.serve(handler, "0.0.0.0", 8765):
        await broadcast_loop(tokens, engine)


if __name__ == "__main__":
    asyncio.run(main())
