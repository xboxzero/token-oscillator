# Web Instrument for Meditation

Real-time audiovisual meditation instrument on Raspberry Pi 5. Streams simulated multi-token data through Lorenz/Fourier/sine oscillators and renders a 3D circle-of-life scene with procedural animals orbiting a glowing core, driven by a digital synthesizer and music-theory-based engine you can play live.

![Stack](https://img.shields.io/badge/stack-Python%20%2B%20Three.js%20%2B%20WebAudio-blue)
![Platform](https://img.shields.io/badge/platform-Raspberry%20Pi%205-red)

## What It Does

**Backend** (Python + WebSocket)
- Simulates 8 token price feeds (ETH, BTC, SOL, LINK, UNI, AAVE, ARB, OP) at 10Hz
- Runs Lorenz attractor, 64-sample rolling FFT, and 3-layer sine oscillator on token deltas
- Compresses 4th dimension (w) into HSL color/opacity values
- Broadcasts JSON via WebSocket at `ws://host:8765`

**3D Circle of Life Visuals** (Three.js + GLSL)
- Toroidal ring path — the "circle of life" — with 8 procedural 3D animals orbiting:
  - **Deer** — body, legs, neck, head, antlers
  - **Fish** (x2) — ellipsoid body, tail fin, dorsal fin, eyes
  - **Bird** (x2) — body, head, beak, flapping wings, tail
  - **Turtle** — dome shell, belly, legs, head, tail
  - **Elephant** — body, trunk (articulated), legs, ears, tusks, tail
  - **Butterfly** — body with 4 translucent wings that flutter
- All animals shift color based on the melody you play
- Drum hits pulse animal scale and bloom intensity
- Glowing center orb with GLSL shader (hue + pulse from melody)
- 2 waveform ribbons circling the ring — undulate with keyboard notes
- 6,000 stars + 4,000 dust particles along the ring
- UnrealBloom post-processing synced to playing dynamics
- Slow orbiting camera with vertical bob

**Digital Synthesizer** (Web Audio API)
- **4 waveforms**: Sine, Sawtooth, Square, Triangle
- **3-oscillator unison** with slight detune for richness
- **Sub oscillator** (1 octave down, sine)
- **Filter**: lowpass with cutoff + resonance controls
- **ADSR envelope**: Attack + Release sliders
- Playable via keyboard (Z-/ white keys, S D G H J L ; black keys)

**Music Engine**
- **Jazz drums**: ride cymbal swing, kick/snare with ghost notes, hi-hat
- **Thai drums**: klong, ching (open/closed), ranat xylophone (scale-aware)
- **Ethiopian drums**: kebero (low/high), shaker
- **Walking bass**: 3 modes — Walk (chromatic approaches), Root, 1-5 (root-fifth)
- **Dub siren**: hold-to-play sawtooth siren with LFO wobble
- **7 scales**: Major, Dorian, Mixolydian, Minor, Blues, Pentatonic, Tizita
- **7 keys**: C, D, E, F, G, A, B — everything transposes together
- **FX chain**: overdrive → phaser → convolution reverb → feedback delay

## Keyboard Layout

Play the synth using your computer keyboard:

```
 S D   G H J   L ;        ← black keys
Z X C V B N M , . /       ← white keys (C D E F G A B C D E)
```

Or click the on-screen keys. Touch-friendly on mobile/tablet.

## Synth Controls

| Control | Function |
|---------|----------|
| SIN / SAW / SQR / TRI | Oscillator waveform |
| CUT | Filter cutoff (lowpass) |
| RES | Filter resonance |
| ATK | Attack time (0–2s) |
| REL | Release time (0–3s) |

## FX Chain

Signal path: **synth → overdrive → phaser → reverb + delay → master**

| FX | Control | Description |
|----|---------|-------------|
| DRIVE | 0–100% | Waveshaper overdrive with variable curve |
| PHASE | 0–100% | 4-stage allpass phaser with LFO |
| VERB | 0–100% | Convolution reverb (2.2s decay) |
| ECHO | 0–100% | Feedback delay (350ms, ~30% feedback) |

## Recording & Download

1. Click **REC** to start recording all audio output
2. Click **REC** again to stop
3. Click **SAVE** to download the recording as `.webm`

Records everything: synth, drums, bass, drone, siren, microphone input, and FX.

## Microphone / External Input

1. Click **MIC** to connect your microphone or audio interface
2. Adjust **GAIN** (0–200%) for input level
3. Use **LO** and **HI** shelving EQ filters (-12dB to +12dB)
4. Level meter shows real-time input signal
5. Mic audio goes through the full FX chain
6. Mic is included in recordings

## Live Performance Controls

### Transport Bar
| Control | Function |
|---------|----------|
| BPM slider | 50–180 BPM |
| TAP | Tap tempo (3+ taps) |
| Scale | Major, Dorian, Mixolydian, Minor, Blues, Pentatonic, Tizita |
| Key | C, D, E, F, G, A, B (transposes everything) |
| REC / SAVE | Record and download audio |
| VOL | Master volume |

### Drums
- **ON/OFF** toggle
- **Jazz / Thai / Ethio** drum styles
- **Kick / Snare / Hat** individual volumes
- **Swing** amount + overall **Volume**

### Bass
- **ON/OFF** toggle
- **Walk / Root / 1-5** patterns
- **Volume** and **Tone** (filter cutoff)

### UI Controls
- **Fullscreen** button (top-right corner)
- **Panel toggle** button (bottom-right) — hide controls for immersive visual mode

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
