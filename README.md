# Token Oscillator

Real-time Web3 token data visualizer running on Raspberry Pi 5. A live-performance audiovisual instrument that streams simulated multi-token price data through mathematical oscillators (Lorenz attractor, Fourier, sine banks) and renders the output as a 3D solar system with flying dragons, driven by a jazz/world-music engine you can play live.

![Stack](https://img.shields.io/badge/stack-Python%20%2B%20Three.js%20%2B%20WebAudio-blue)
![Platform](https://img.shields.io/badge/platform-Raspberry%20Pi%205-red)

## What It Does

**Backend** (Python + WebSocket)
- Simulates 8 token price feeds (ETH, BTC, SOL, LINK, UNI, AAVE, ARB, OP) at 10Hz
- Runs Lorenz attractor, 64-sample rolling FFT, and 3-layer sine oscillator on token deltas
- Compresses 4th dimension (w) into HSL color/opacity values
- Broadcasts all data as JSON via WebSocket at `ws://host:8765`

**Frontend** (Three.js + GLSL + Web Audio API)
- 3D solar system: sun with GLSL corona shader, 8 orbiting planets mapped to tokens
- 5 procedural dragons flying through the system with flapping wings and fire breath
- 8,000 star background + 8,000 particle dust belt
- Token data drives: orbit speed, planet size, color shifts, bloom intensity
- Drum hits trigger: camera shake, particle push, bloom flash, dragon fire bursts

**Music Engine** (Web Audio API, music-theory based)
- **Jazz drums**: ride cymbal pattern, kick/snare with ghost notes, hi-hat
- **Thai drums**: klong barrel drum, ching cymbal (open/closed), ranat xylophone
- **Ethiopian drums**: kebero (low/high), washint flute (Tizita scale), shaker
- **Walking bass**: scale-aware walking bassline with chromatic approaches
- **Drawbar organ**: playable keyboard with Leslie vibrato effect
- **Scales**: Major, Dorian, Mixolydian, Minor, Blues, Pentatonic, Tizita (Ethiopian), Thai Pentatonic
- **Reverb**: convolution reverb with wet/dry mix

## Live Performance Controls

### Transport Bar (top of panel)
| Control | Function |
|---------|----------|
| BPM slider | 50–180 BPM |
| TAP button | Tap tempo (tap 3+ times) |
| Scale selector | Choose musical scale |
| Key selector | Transpose (C through B) |
| Master volume | Overall output level |

### Drums Section
- **ON/OFF** toggle
- **Jazz / Thai / Ethio** pattern select
- Swing amount + volume

### Bass Section
- **ON/OFF** toggle
- **Walk** (walking bassline) / **Root** (root note only) / **Octave** (root + octave)
- Volume + tone (filter cutoff)

### Organ Keyboard
- Click keys or use computer keyboard: `A S D F G H J K` (white keys), `W E T Y U` (black keys)
- Drawbar organ tone with Leslie vibrato
- Follows selected scale and key

### Drone/FX Section
- Drone ON/OFF + level
- Reverb wet/dry mix

## Setup

### Requirements
- Raspberry Pi 5 (or any Linux machine)
- Python 3.10+ with `websockets` and `numpy`
- Nginx
- A modern browser (Chromium recommended)

### Quick Install

```bash
git clone https://github.com/xboxzero/token-oscillator.git
cd token-oscillator
chmod +x install.sh
./install.sh
```

The install script will:
1. Install Python `websockets` package
2. Install and configure Nginx
3. Set up a systemd service for auto-start on boot
4. Start everything

### Manual Setup

```bash
# Install deps
pip3 install websockets

# Start backend
python3 backend/server.py &

# Serve frontend (any HTTP server works)
cd frontend && python3 -m http.server 8080
```

Open `http://<your-ip>` in a browser. Click anywhere to start audio.

### Password

The Nginx config includes HTTP Basic Auth:
- **Username:** `oscillator`
- **Password:** `2475112`

To change or remove, edit `/etc/nginx/.htpasswd` or remove `auth_basic` from `nginx.conf`.

## Architecture

```
token-oscillator/
├── backend/
│   └── server.py              # WebSocket server + mock data + oscillator math
├── frontend/
│   ├── index.html             # Single-file app (Three.js + GLSL + Web Audio)
│   ├── three.min.js           # Three.js r152
│   └── pp/                    # Post-processing (UnrealBloom)
├── nginx.conf                 # Nginx site config
├── token-oscillator.service   # systemd unit file
├── install.sh                 # One-shot installer
└── README.md
```

## Service Management

```bash
# Start/stop/restart
sudo systemctl start token-oscillator
sudo systemctl stop token-oscillator
sudo systemctl restart token-oscillator

# View logs
sudo journalctl -u token-oscillator -f

# Check status
systemctl status token-oscillator
```

## Performance

On Raspberry Pi 5:
- Backend: ~0.5% CPU (asyncio at 10Hz)
- Frontend: targets 30fps with 20k+ objects
- Total idle: well under 40% CPU

## License

MIT
