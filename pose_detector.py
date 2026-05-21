import numpy as np

def calc_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    ba = a - b
    bc = c - b
    cos_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6)
    return float(np.degrees(np.arccos(np.clip(cos_angle, -1.0, 1.0))))

def get_landmarks(lms, lm_ids, w, h):
    def pt(lm_id):
        lm = lms[lm_id]
        return [lm.x * w, lm.y * h]
    return pt(lm_ids[0]), pt(lm_ids[1]), pt(lm_ids[2])

def detect_touch_face(lms, w, h):
    import mediapipe as mp
    _lm = mp.solutions.pose.PoseLandmark
    nose  = lms[_lm.NOSE]
    wrist = lms[_lm.LEFT_WRIST]
    dist  = ((wrist.x - nose.x) * w) ** 2 + ((wrist.y - nose.y) * h) ** 2
    return dist ** 0.5 < 80
