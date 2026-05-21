import json
import os
from datetime import date
from config import PLAYER_FILE, LEVELS

# ── default player state ──────────────────────────────────────
def _default():
    return {
        "name":          "",
        "total_xp":      0,
        "total_reps":    0,
        "total_sessions":0,
        "streak":        0,
        "last_session":  "",
        "bests": {
            "Bicep Curl":     {"reps": 0, "date": ""},
            "Squat":          {"reps": 0, "date": ""},
            "Shoulder Press": {"reps": 0, "date": ""},
        },
    }

# ── load / save ───────────────────────────────────────────────
def load_player():
    if os.path.exists(PLAYER_FILE):
        try:
            with open(PLAYER_FILE) as f:
                data = json.load(f)
            # back-fill any missing keys
            default = _default()
            for k, v in default.items():
                if k not in data:
                    data[k] = v
            return data
        except Exception:
            pass
    return _default()

def save_player(player):
    with open(PLAYER_FILE, "w") as f:
        json.dump(player, f, indent=2)

# ── level lookup ──────────────────────────────────────────────
def get_level(xp):
    level = LEVELS[0]
    for lv in LEVELS:
        if xp >= lv["min_xp"]:
            level = lv
    idx = LEVELS.index(level)
    next_lv = LEVELS[idx + 1] if idx + 1 < len(LEVELS) else None
    return level, next_lv, idx

# ── award xp for a rep ────────────────────────────────────────
def award_rep(player, xp_amount):
    old_level, _, _ = get_level(player["total_xp"])
    player["total_xp"]   += xp_amount
    player["total_reps"] += 1
    new_level, _, _       = get_level(player["total_xp"])
    leveled_up = new_level["name"] != old_level["name"]
    return leveled_up, new_level["name"]

# ── update streak & session count ────────────────────────────
def update_streak(player):
    today     = str(date.today())
    last      = player.get("last_session", "")
    yesterday = str(date.fromordinal(date.today().toordinal() - 1))
    if last == today:
        pass                         # already counted today
    elif last == yesterday:
        player["streak"] += 1        # kept the streak alive
    else:
        player["streak"] = 1         # streak broken or first session
    player["last_session"]   = today
    player["total_sessions"] += 1

# ── update personal best ──────────────────────────────────────
def update_best(player, exercise_name, reps):
    today = str(date.today())
    bests = player.setdefault("bests", {})
    if exercise_name not in bests:
        bests[exercise_name] = {"reps": 0, "date": ""}
    if reps > bests[exercise_name]["reps"]:
        bests[exercise_name] = {"reps": reps, "date": today}
        return True
    return False
