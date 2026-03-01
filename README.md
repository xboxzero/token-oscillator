# Clouding Synthesizer

Open-source multi-player web instrument for live performance, meditation, and sound exploration. Runs on any machine — Raspberry Pi, laptop, or cloud server. Multiple players connect from different machines for collaborative jam sessions and battle mode.

![Stack](https://img.shields.io/badge/stack-Python%20%2B%20Three.js%20%2B%20WebAudio-blue)
![Platform](https://img.shields.io/badge/platform-Any%20Machine-green)
![License](https://img.shields.io/badge/license-MIT-yellow)
![Players](https://img.shields.io/badge/multiplayer-battle%20mode-red)

## Features

### Multi-Player Battle Mode
- **Room-based WebSocket** — all players on the same server share a room
- **Real-time state sync** — see who's playing, what notes, which FX
- **Player badges** — color-coded with live status indicators
- **Cross-machine** — connect from any device on the network

### 3D Circle of Life Visuals (Three.js + GLSL)
- **Auto-generating 3D animals** — deer, fish, bird, turtle, elephant, butterfly, whale, fox
- New animals spawn every 12 seconds, up to 10 on screen
- Animals orbit a toroidal "circle of life" ring
- **Color shifts with melody** — each note changes the hue of all animals
- GLSL-shaded center orb pulses with amplitude
- 2 waveform ribbons circle the ring, undulating with keyboard notes
- Drum hits pulse scale + bloom intensity
- UnrealBloom post-processing, orbiting camera, 5k stars, 3k dust

### Digital Synthesizer
- **4 waveforms**: Sine, Sawtooth, Square, Triangle
- **3-oscillator unison** with detune for richness + sub oscillator
- **Filter**: lowpass with cutoff + resonance
- **ADSR**: attack + release envelope
- Playable via keyboard or on-screen keys

### Reggae / Dub / Dancehall Drums
- **One Drop** — classic reggae (kick + snare on beat 3)
- **Steppers** — 4-on-the-floor roots reggae
- **Dancehall** — syncopated kick, clap, fast hi-hats
- **Dub** — heavy sparse kick, rimshot, space
- **Percussion**: hi-hat (open/closed), rimshot, clap, tambourine, percussion hit
- Per-instrument volume: kick, snare, hi-hat, percussion

### Bass
- **Reggae** — walking bass with chromatic approaches
- **Dub** — sparse offbeat hits with sub
- **Root** — simple root note
- Sub bass level control

### FX Chain with ON/OFF Buttons
Each effect has a dedicated **ON/OFF toggle** button:
- **DRV** (Overdrive) — waveshaper with variable curve
- **PHA** (Phaser) — 4-stage allpass with LFO
- **REV** (Reverb) — convolution reverb (2.5s decay)
- **DLY** (Delay) — feedback delay (380ms, 35% feedback)
- **DUB SIREN** — hold-to-play sawtooth + LFO wobble
- FX section border **auto-color cycles** with the melody

### Mixer with EQ
Full mixer with per-channel controls:
| Channel | Controls |
|---------|----------|
| SYN (Synth) | Volume + 3-band EQ (Lo/Mid/Hi) |
| DRM (Drums) | Volume + 3-band EQ (Lo/Mid/Hi) |
| BAS (Bass) | Volume + 3-band EQ (Lo/Mid/Hi) |
| MIC (Microphone) | Volume + 2-band EQ (Lo/Hi) |

### Recording & Microphone
- **REC / SAVE** — record all audio output, download as `.webm`
- **MIC** — connect microphone/audio interface with gain control
- Mic routes through the mixer and full FX chain

### 8-Bit Solarpunk UI
- Pixel art inspired design with **Press Start 2P** font
- Green / gold / earth tone color scheme
- Retro pixel borders and glowing buttons
- Auto-color cycling on FX section
- Fullscreen button + panel toggle for immersive mode

## Keyboard Layout

```
 S D   G H J   L ;        ← black keys
Z X C V B N M , . /       ← white keys (C D E F G A B C D E)
```

## Multi-Player Setup

### Host Machine (Server)
```bash
git clone https://github.com/xboxzero/token-oscillator.git
cd token-oscillator
pip3 install websockets numpy
python3 backend/server.py
```

### Other Players (Clients)
Open `http://SERVER_IP` in any browser. Everyone on the same network can join.

Each player gets:
- Unique color badge
- Real-time note/FX state broadcast to all others
- Independent instrument controls

### Battle Mode
When 2+ players are connected:
- Player badges appear in the top-left corner
- Each player's active notes are shown
- All players hear their own instruments independently
- The 3D visuals react to the local player's melody

## Quick Install (Raspberry Pi with Nginx)

```bash
git clone https://github.com/xboxzero/token-oscillator.git
cd token-oscillator
chmod +x install.sh
./install.sh
```

### Password (Nginx)
- **Username:** `oscillator`
- **Password:** `2475112`

## Architecture

```
token-oscillator/
├── backend/
│   └── server.py              # Multi-player WebSocket server + oscillator
├── frontend/
│   ├── index.html             # Single-file app (Three.js + Web Audio)
│   ├── three.min.js           # Three.js library
│   └── pp/                    # Post-processing (UnrealBloom)
├── nginx.conf                 # Nginx config with auth
├── token-oscillator.service   # systemd unit
├── install.sh                 # Installer
└── README.md
```

## Run Anywhere

```bash
# Any machine with Python 3 + Node/browser:
pip3 install websockets numpy
python3 backend/server.py &
cd frontend && python3 -m http.server 8080
# Open http://localhost:8080
```

## Service Management

```bash
sudo systemctl start token-oscillator
sudo systemctl stop token-oscillator
sudo systemctl restart token-oscillator
sudo journalctl -u token-oscillator -f
```

## License

MIT — open source, run it anywhere, modify freely.
