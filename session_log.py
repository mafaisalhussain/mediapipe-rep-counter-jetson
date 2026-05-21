import json
import os
from datetime import datetime
from config import SESSION_DIR

def save_session(exercise_name, sets_data, total_cals, total_xp, tempo_summary):
    os.makedirs(SESSION_DIR, exist_ok=True)
    ts       = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{ts}_{exercise_name.replace(' ', '_')}.json"
    path     = os.path.join(SESSION_DIR, filename)
    payload  = {
        "exercise":      exercise_name,
        "date":          datetime.now().strftime("%Y-%m-%d"),
        "time":          datetime.now().strftime("%H:%M"),
        "sets":          sets_data,     # list of {"set": n, "reps": n}
        "total_cals":    round(total_cals, 2),
        "total_xp":      total_xp,
        "tempo":         tempo_summary,
    }
    with open(path, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"  Session saved → {filename}")
    return path

def load_recent_sessions(n=10):
    if not os.path.exists(SESSION_DIR):
        return []
    files = sorted(
        [f for f in os.listdir(SESSION_DIR) if f.endswith(".json")],
        reverse=True
    )[:n]
    sessions = []
    for fname in files:
        try:
            with open(os.path.join(SESSION_DIR, fname)) as f:
                sessions.append(json.load(f))
        except Exception:
            pass
    return sessions
