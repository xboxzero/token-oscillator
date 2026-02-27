# Token Oscillator

Real-time Web3 token data visualizer and live-performance audiovisual instrument on Raspberry Pi 5. Streams simulated multi-token price data through Lorenz/Fourier/sine oscillators and renders a 3D solar system with organic space creatures, driven by a music-theory-based engine you can play live with recording and microphone support.

![Stack](https://img.shields.io/badge/stack-Python%20%2B%20Three.js%20%2B%20WebAudio-blue)
![Platform](https://img.shields.io/badge/platform-Raspberry%20Pi%205-red)

## What It Does

**Backend** (Python + WebSocket)
- Simulates 8 token price feeds (ETH, BTC, SOL, LINK, UNI, AAVE, ARB, OP) at 10Hz
- Runs Lorenz attractor, 64-sample rolling FFT, and 3-layer sine oscillator on token deltas
- Compresses 4th dimension (w) into HSL color/opacity values
- Broadcasts JSON via WebSocket at `ws://host:8765`

**3D Visuals** (Three.js + GLSL)
- Solar system: GLSL-shaded sun with corona, 8 orbiting planets mapped to tokens
- 3 **space whales** — ellipsoid bodies with pectoral fins, tail flukes, belly glow, organic swimming motion
- 2 **phoenix birds** — tapered bodies with wide flapping wings, tail feathers, fire trail sprites
- All creatures orbit independently, react to drum hits (fin sweep, wing flap, fire burst)
- 8,000 stars + 8,000 dust belt particles
- UnrealBloom post-processing synced to drum impacts

**Music Engine** (Web Audio API)
- **Jazz drums**: ride cymbal swing, kick/snare with ghost notes, hi-hat — individual volume per instrument (kick, snare, hat)
- **Thai drums**: klong, ching (open/closed), ranat xylophone (scale-aware)
- **Ethiopian drums**: kebero (low/high), washint flute (Tizita scale), shaker
- **Walking bass**: 4 modes — Walk (chromatic approaches), Root, Octave, 1-5 (root-fifth)
- **Drawbar organ**: 5-harmonic synthesis with Leslie vibrato, playable via keyboard
- **8 scales**: Major, Dorian, Mixolydian, Minor, Blues, Pentatonic, Tizita, Thai
- **12 keys**: C through B — everything transposes together
- **FX**: convolution reverb + feedback delay with wet/dry controls

## Keyboard Layout

Play the organ using your computer keyboard:

```
 S D   G H J   L ;        ← black keys (Db Eb Gb Ab Bb Db Eb)
Z X C V B N M , . /       ← white keys (C D E F G A B C D E)
```

Or click the on-screen keys. Touch-friendly on mobile/tablet.

## Recording & Download

1. Click **REC** to start recording all audio output
2. Click **REC** again to stop
3. Click **SAVE WAV** to download the recording as `.webm`

Records everything: drums, bass, organ, drone, microphone input, and FX.

## Microphone / External Input

1. Click **MIC** to connect your microphone or audio interface
2. Adjust **GAIN** (0–200%) for input level
3. Use **EQ LO** and **EQ HI** shelving filters (-12dB to +12dB)
4. The level meter shows real-time input signal
5. Mic audio goes through the same reverb/delay FX chain
6. Mic is included in recordings

Works with built-in mics, USB audio interfaces, or Bluetooth headsets.

## Live Performance Controls

### Transport Bar
| Control | Function |
|---------|----------|
| BPM slider | 50–180 BPM |
| TAP | Tap tempo (3+ taps) |
| Scale | Major, Dorian, Mixolydian, Minor, Blues, Pentatonic, Tizita, Thai |
| Key | C through B (transposes everything) |
| REC / SAVE | Record and download audio |
| Master | Overall volume |

### Drums
- **ON/OFF** toggle
- **Jazz / Thai / Ethio** styles
- **Swing** amount
- **Kick / Snare / Hat** individual volumes

### Bass
- **ON/OFF** toggle
- **Walk / Root / Octave / 1-5** patterns
- **Volume, Tone** (filter), **Octave** (Low/Mid/Hi)

### Organ
- Playable keyboard (click or PC keys)
- Drawbar organ with Leslie effect

### Mic / Input
- **MIC** on/off with level meter
- **Gain** control (0–200%)
- **EQ Low / High** shelving

### FX / Drone
- **Drone** on/off with level
- **Reverb** wet/dry
- **Delay** wet/dry

## Setup

### Quick Install (Raspberry Pi)

```bash
git clone https://github.com/xboxzero/token-oscillator.git
cd token-oscillator
chmod +x install.sh
./install.sh
```

Starts everything and enables auto-start on boot.

### Manual Setup (any machine)

```bash
pip3 install websockets numpy
python3 backend/server.py &
cd frontend && python3 -m http.server 8080
```

Open `http://localhost:8080`. Click anywhere to start audio.

### Password

Nginx HTTP Basic Auth:
- **Username:** `oscillator`
- **Password:** `2475112`

Edit `/etc/nginx/.htpasswd` to change, or remove `auth_basic` from `nginx.conf`.

## Architecture

```
token-oscillator/
├── backend/
│   └── server.py              # WebSocket server + mock data + oscillator math
├── frontend/
│   ├── index.html             # Single-file app (Three.js + GLSL + Web Audio)
│   ├── three.min.js           # Three.js library
│   └── pp/                    # Post-processing (UnrealBloom)
├── nginx.conf                 # Nginx site config with auth
├── token-oscillator.service   # systemd unit file
├── install.sh                 # One-shot installer
└── README.md
```

## Service Management

```bash
sudo systemctl start token-oscillator     # start
sudo systemctl stop token-oscillator      # stop
sudo systemctl restart token-oscillator   # restart
sudo journalctl -u token-oscillator -f    # logs
```

## Performance

On Raspberry Pi 5: backend ~0.5% CPU, frontend targets 30fps. Total < 40% CPU.

## License

MIT
