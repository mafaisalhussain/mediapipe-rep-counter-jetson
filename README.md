# Real-Time Exercise Rep Counter — Jetson Nano

A fully offline, real-time exercise repetition counter running on a **Jetson Nano 4GB** using only a camera. No cloud, no training, no wearables.

## How it works

1. Camera captures a live frame
2. **MediaPipe Pose** (pre-trained) detects 33 body landmarks
3. Joint angles are computed from 3 landmark coordinates
4. A state machine counts reps: `extended → contracted = 1 rep`
5. Live overlay displays rep count, angle, and feedback

## Supported exercises

| Exercise    | Joint tracked        |
|-------------|----------------------|
| Bicep Curl  | Shoulder → Elbow → Wrist |
| Push Up     | Shoulder → Elbow → Wrist |
| Squat       | Hip → Knee → Ankle   |

## Project structure

```
rep_counter/
├── main.py           # Entry point — camera loop
├── pose_detector.py  # MediaPipe Pose wrapper + angle math
├── rep_counter.py    # State machine (up/down → rep count)
├── overlay.py        # OpenCV UI overlay on frame
├── config.py         # Exercise definitions + thresholds
└── requirements.txt
```

## Setup on Jetson Nano

```bash
pip3 install opencv-python mediapipe numpy
```

> For JetPack 4.x use the community MediaPipe build:
> https://github.com/PINTO0309/mediapipe-bin

## Run

```bash
cd rep_counter
python3 main.py
```

## Controls

| Key | Action            |
|-----|-------------------|
| `Q` | Quit              |
| `R` | Reset rep count   |
| `E` | Switch exercise   |

## Hardware

- Jetson Nano 4GB (JetPack 4.6)
- USB webcam or Raspberry Pi Camera v2 (CSI)
- 720p recommended for best FPS
