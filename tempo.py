import time
from config import TEMPO_FAST, TEMPO_SLOW

class TempoTracker:
    def __init__(self):
        self._last_rep_time = None
        self._history       = []   # last 5 rep durations
        self.last_duration  = None
        self.avg_pace       = None # avg seconds/rep
        self.label          = ""   # "fast" / "steady" / "slow"

    def record_rep(self):
        now = time.time()
        if self._last_rep_time is not None:
            duration = now - self._last_rep_time
            self._history.append(duration)
            if len(self._history) > 5:
                self._history.pop(0)
            self.last_duration = duration
            self.avg_pace      = sum(self._history) / len(self._history)
            if duration < TEMPO_FAST:
                self.label = "fast"
            elif duration > TEMPO_SLOW:
                self.label = "slow"
            else:
                self.label = "steady"
        self._last_rep_time = now

    def reset(self):
        self._last_rep_time = None
        self._history       = []
        self.last_duration  = None
        self.avg_pace       = None
        self.label          = ""

    def summary(self):
        return {
            "avg_pace_sec": round(self.avg_pace, 2) if self.avg_pace else None,
            "rep_durations": [round(d, 2) for d in self._history],
        }
