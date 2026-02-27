# Token Oscillator

Real-time Web3 token data visualizer and live-performance audiovisual instrument on Raspberry Pi 5. Streams simulated multi-token price data through Lorenz/Fourier/sine oscillators and renders flowing waveform visuals that react to your keyboard playing, driven by a music-theory-based engine with full FX chain, recording, and microphone support.

![Stack](https://img.shields.io/badge/stack-Python%20%2B%20Canvas%20%2B%20WebAudio-blue)
![Platform](https://img.shields.io/badge/platform-Raspberry%20Pi%205-red)

## What It Does

**Backend** (Python + WebSocket)
- Simulates 8 token price feeds (ETH, BTC, SOL, LINK, UNI, AAVE, ARB, OP) at 10Hz
- Runs Lorenz attractor, 64-sample rolling FFT, and 3-layer sine oscillator on token deltas
- Compresses 4th dimension (w) into HSL color/opacity values
- Broadcasts JSON via WebSocket at `ws://host:8765`

**Flowing Waveform Visuals** (Canvas 2D)
- 18 layered sine waveforms flowing across the screen like colored water
- Keyboard-driven: each note maps to a unique hue, amplitude, and wave frequency
- Multi-layer composition: melody sine + backend Lorenz + bass pulse + drum hits
- Fourier spectrum rendered as vertical glow bars
- Drum hits create visual shockwaves across all wave lines
- Bass notes pulse the waveform vertically
- Dub siren pushes hue to orange and maxes amplitude
- Smooth interpolation — all transitions feel organic

**Music Engine** (Web Audio API)
- **Jazz drums**: ride cymbal swing, kick/snare with ghost notes, hi-hat — individual volume per instrument
- **Thai drums**: klong, ching (open/closed), ranat xylophone (scale-aware)
- **Ethiopian drums**: kebero (low/high), shaker
- **Walking bass**: 3 modes — Walk (chromatic approaches), Root, 1-5 (root-fifth)
- **Drawbar organ**: 5-harmonic synthesis with Leslie vibrato, playable via keyboard
- **Dub siren**: hold-to-play sawtooth siren with LFO wobble
- **7 scales**: Major, Dorian, Mixolydian, Minor, Blues, Pentatonic, Tizita
- **7 keys**: C, D, E, F, G, A, B — everything transposes together
- **FX chain**: overdrive (waveshaper) → phaser (4-stage allpass + LFO) → convolution reverb → feedback delay

## Keyboard Layout

Play the organ using your computer keyboard:

```
 S D   G H J   L ;        ← black keys
Z X C V B N M , . /       ← white keys (C D E F G A B C D E)
```

Or click the on-screen keys. Touch-friendly on mobile/tablet.

## FX Chain

Signal path: **instrument → overdrive → phaser → reverb + delay → master**

| FX | Control | Description |
|----|---------|-------------|
| DRIVE | 0–100% | Waveshaper overdrive with variable distortion curve |
| PHASE | 0–100% | 4-stage allpass phaser with sine LFO modulation |
| VERB | 0–100% | Convolution reverb (1.8s decay) |
| ECHO | 0–100% | Feedback delay (350ms, ~30% feedback) |

All FX sliders are in the **FX Chain** panel section.

## Dub Siren

Hold the **DUB SIREN** button (mouse or touch) to activate. Releases when you let go. Sawtooth oscillator with sine LFO on frequency — classic dub/reggae siren sound. Goes through the full FX chain.

## Recording & Download

1. Click **REC** to start recording all audio output
2. Click **REC** again to stop
3. Click **SAVE** to download the recording as `.webm`

Records everything: drums, bass, organ, drone, siren, microphone input, and FX.

## Microphone / External Input

1. Click **MIC** to connect your microphone or audio interface
2. Adjust **GAIN** (0–200%) for input level
3. Use **LO** and **HI** shelving EQ filters (-12dB to +12dB)
4. The level meter shows real-time input signal
5. Mic audio goes through the full FX chain (overdrive, phaser, reverb, delay)
6. Mic is included in recordings

Works with built-in mics, USB audio interfaces, or Bluetooth headsets.

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
- **Swing** amount
- **Volume** overall drum level

### Bass
- **ON/OFF** toggle
- **Walk / Root / 1-5** patterns
- **Volume** and **Tone** (filter cutoff)

### Organ
- Playable keyboard (click or PC keys)
- 5-harmonic drawbar synthesis with Leslie vibrato

### FX Chain
- **Drive** — overdrive intensity
- **Phase** — phaser wet mix
- **Verb** — reverb wet mix
- **Echo** — delay wet mix
- **DUB SIREN** — hold to play

### Mic / Input
- **MIC** on/off with level meter
- **Gain** control (0–200%)
- **LO / HI** shelving EQ

### UI Controls
- **Fullscreen** button (top-right corner)
- **Panel toggle** button (bottom-right) — hide/show controls for clean visual mode

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
│   └── index.html             # Single-file app (Canvas + Web Audio + FX chain)
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

On Raspberry Pi 5: backend ~0.5% CPU, frontend targets 30fps with Canvas 2D. Total < 40% CPU.

## License

MIT
