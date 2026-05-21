import os

# ── user ──────────────────────────────────────────────────────
print("\n" + "="*46)
print("      REP COUNTER — Powered by MediaPipe")
print("="*46)
USER_NAME = input("  Enter your name: ").strip()
if not USER_NAME:
    USER_NAME = "Athlete"
print(f"\n  Welcome, {USER_NAME}!\n")

# ── paths ─────────────────────────────────────────────────────
BASE_DIR    = os.path.expanduser("~/Desktop/AIproj")
MEME_DIR    = os.path.join(BASE_DIR, "memes")
SESSION_DIR = os.path.join(BASE_DIR, "sessions")
PLAYER_FILE = os.path.join(BASE_DIR, "player.json")

for d in [MEME_DIR, SESSION_DIR]:
    os.makedirs(d, exist_ok=True)

# ── layout ────────────────────────────────────────────────────
PANEL_W = 200
BAR_H   = 36

# ── colors (BGR) ──────────────────────────────────────────────
ACCENT  = (127, 119, 221)
GREEN   = (0,   230, 118)
CYAN    = (0,   255, 255)
YELLOW  = (0,   235, 255)
WHITE   = (255, 255, 255)
GRAY    = (120, 120, 120)
BLACK   = (0,   0,   0)
ORANGE  = (0,   165, 255)
RED     = (0,   0,   220)

# ── exercises ─────────────────────────────────────────────────
import mediapipe as mp
_lm = mp.solutions.pose.PoseLandmark

EXERCISES = {
    "1": {
        "name":        "Bicep Curl",
        "landmarks":   [_lm.LEFT_SHOULDER, _lm.LEFT_ELBOW, _lm.LEFT_WRIST],
        "up_angle":    160,
        "down_angle":  40,
        "cal_per_rep": 0.08,
        "xp_per_rep":  2,
    },
    "2": {
        "name":        "Squat",
        "landmarks":   [_lm.LEFT_HIP, _lm.LEFT_KNEE, _lm.LEFT_ANKLE],
        "up_angle":    160,
        "down_angle":  90,
        "cal_per_rep": 0.32,
        "xp_per_rep":  5,
    },
    "3": {
        "name":        "Shoulder Press",
        "landmarks":   [_lm.LEFT_ELBOW, _lm.LEFT_SHOULDER, _lm.LEFT_HIP],
        "up_angle":    160,
        "down_angle":  70,
        "cal_per_rep": 0.10,
        "xp_per_rep":  3,
    },
}

# ── rep goals (for progress bar) ──────────────────────────────
GOALS = [8, 12, 15, 20, 25]

# ── gamification: levels ──────────────────────────────────────
LEVELS = [
    {"name": "Rookie",  "min_xp": 0},
    {"name": "Iron",    "min_xp": 200},
    {"name": "Bronze",  "min_xp": 500},
    {"name": "Silver",  "min_xp": 1000},
    {"name": "Gold",    "min_xp": 1500},
]

# ── tempo thresholds (seconds per rep) ────────────────────────
TEMPO_FAST   = 1.5   # faster than this = fast
TEMPO_SLOW   = 4.0   # slower than this = slow

# ── dashboard server port ─────────────────────────────────────
DASHBOARD_PORT = 5500

# ── motivation messages ───────────────────────────────────────
def get_motivation(reps, name):
    msgs = {
        1:  f"Let's go {name}!",
        5:  "Warming up!",
        8:  "8 reps — beast mode!",
        10: "10! Keep pushing!",
        12: "12 reps — unstoppable!",
        15: f"15!! You're on fire {name}!",
        20: "20 REPS. LEGENDARY.",
    }
    return msgs.get(reps, None)
