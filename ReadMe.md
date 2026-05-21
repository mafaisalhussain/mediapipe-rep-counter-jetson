# AI Fitness Rep Counter

A real-time AI-powered workout tracker built with **Python**, **OpenCV**, and **MediaPipe Pose Detection**.
The system tracks exercise reps through webcam posture analysis, awards XP, measures workout tempo, logs sessions, and provides a live dashboard with gamification features.

---

## Features

- Real-time pose detection using MediaPipe
- Automatic rep counting
- Support for multiple exercises
- Live workout HUD overlay
- Gamification system with XP and levels
- Workout streak tracking
- Tempo analysis (fast / steady / slow)
- Personal best tracking
- Session logging in JSON format
- Browser dashboard for analytics
- Meme reward system during workouts
- Lightweight local web dashboard
- Modular and extensible architecture

---

## Supported Exercises

Currently supported exercises:

- Bicep Curl
- Squat
- Shoulder Press

Each exercise has:

- Dedicated pose landmarks
- Angle thresholds
- XP rewards
- Calorie estimation

---

## Project Structure

```text
.
├── main.py                # Main application loop
├── config.py              # Configuration and exercise settings
├── pose_detector.py       # Pose and angle calculations
├── overlay.py             # Workout UI rendering
├── gamification.py        # XP, streaks, levels, bests
├── session_log.py         # Workout session storage
├── dashboard.py           # Local dashboard server
├── dashboard.html         # Dashboard frontend
├── tempo.py               # Tempo analysis system
├── player.json            # Player progress data
├── media/                 # All project media assets
├── sessions/              # Saved workout sessions
└── memes/                 # Meme reward images
```

---

# How It Works

The webcam feed is processed using MediaPipe Pose Detection.

For every frame:

1. Body landmarks are detected
2. Joint angles are calculated
3. Movement thresholds determine rep completion
4. XP and stats are updated
5. UI overlays are rendered in real time

---

# Gamification System

The application includes a full progression system.

## XP & Levels

Users gain XP for every rep performed.

Available levels:

- Rookie
- Iron
- Bronze
- Silver
- Gold

---

## Streak Tracking

Daily workout streaks are automatically tracked.

The system:
- Maintains consecutive workout days
- Resets broken streaks
- Updates session history

---

## Personal Bests

The app stores personal best rep counts for each exercise.

Example:

```json
{
  "Bicep Curl": {
    "reps": 13,
    "date": "2026-05-18"
  }
}
```

---

# Tempo Tracking

The system measures workout pace dynamically.

Tempo categories:

- Fast
- Steady
- Slow

The tracker calculates:
- Rep durations
- Average pace
- Tempo classification

---

# Dashboard

The project includes a local dashboard served through Python's built-in HTTP server.

Dashboard features:
- XP progress visualization
- Workout streaks
- Session history
- Personal bests
- 30-day activity tracker
- Tempo summaries

Dashboard launches locally at:

```text
http://localhost:5500
```

---

# Installation

## 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ai-fitness-rep-counter.git
cd ai-fitness-rep-counter
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

### Windows

```bash
venv\Scripts\activate
```

### macOS/Linux

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install opencv-python mediapipe numpy
```

---

# Running the Project

Start the application:

```bash
python main.py
```

The dashboard server starts automatically.

---

# Controls

| Key | Action |
|---|---|
| Q | Quit workout |
| D | Open dashboard |

---

# Session Storage

Workout sessions are automatically saved as JSON files.

Each session stores:
- Exercise name
- Sets
- Rep counts
- Calories burned
- XP earned
- Tempo statistics

---

# Exercise Detection Logic

Each exercise uses:
- Specific body landmarks
- Angle thresholds
- State transitions

Example workflow:
1. Detect arm or leg angle
2. Identify "up" movement
3. Detect "down" threshold
4. Increment rep count

---

# Technologies Used

- Python
- OpenCV
- MediaPipe
- NumPy
- HTML/CSS/JavaScript
- HTTPServer

---

# Future Improvements

Potential enhancements:
- Multi-person tracking
- More exercises
- Voice feedback
- Mobile dashboard
- AI form correction
- Cloud sync
- Workout recommendations
- Authentication system
- Database integration
- REST API support

---

# Notes

- All media assets should remain inside the `media/` directory.
- Webcam access is required.
- Best performance is achieved in good lighting conditions.

---

# License

This project is licensed under the MIT License.

---

# Acknowledgements

- MediaPipe Pose
- OpenCV
- Python community

