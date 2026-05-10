import os
import mediapipe as mp

mp_pose = mp.solutions.pose

# ── layout ────────────────────────────────────────────────────
PANEL_W = 180
BAR_H   = 36

# ── colors (BGR) ──────────────────────────────────────────────
ACCENT = (127, 119, 221)
GREEN  = (0, 230, 118)
CYAN   = (0, 255, 255)
YELLOW = (0, 235, 255)
WHITE  = (255, 255, 255)
GRAY   = (120, 120, 120)
BLACK  = (0, 0, 0)

# ── paths ─────────────────────────────────────────────────────
MEME_DIR = os.path.expanduser("~/rep_counter_memes")

# ── goals ─────────────────────────────────────────────────────
GOALS = [8, 12, 15, 20]

# ── exercises ─────────────────────────────────────────────────
EXERCISES = {
    "1": {
        "name": "Bicep Curl",
        "landmarks": [
            mp_pose.PoseLandmark.LEFT_SHOULDER,
            mp_pose.PoseLandmark.LEFT_ELBOW,
            mp_pose.PoseLandmark.LEFT_WRIST,
        ],
        "up_angle":    160,
        "down_angle":   40,
        "cal_per_rep": 0.08,
    },
    "2": {
        "name": "Squat",
        "landmarks": [
            mp_pose.PoseLandmark.LEFT_HIP,
            mp_pose.PoseLandmark.LEFT_KNEE,
            mp_pose.PoseLandmark.LEFT_ANKLE,
        ],
        "up_angle":    160,
        "down_angle":   90,
        "cal_per_rep": 0.32,
    },
    "3": {
        "name": "Shoulder Press",
        "landmarks": [
            mp_pose.PoseLandmark.LEFT_ELBOW,
            mp_pose.PoseLandmark.LEFT_SHOULDER,
            mp_pose.PoseLandmark.LEFT_HIP,
        ],
        "up_angle":    160,
        "down_angle":   70,
        "cal_per_rep": 0.10,
    },
}

def get_motivation(reps, user_name):
    milestones = {
        1:  f"Let's GO {user_name}!",
        5:  "Warming up...",
        8:  "BEAST MODE!",
        12: "UNSTOPPABLE!",
        15: f"{user_name} IS GOATED!",
    }
    if reps in milestones:
        return milestones[reps]
    if reps > 15 and reps % 5 == 0:
        return f"{reps} reps?! Superhuman!"
    return None
