import numpy as np
import mediapipe as mp

mp_pose = mp.solutions.pose

def calc_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    cos_val = np.dot(a - b, c - b) / (
        np.linalg.norm(a - b) * np.linalg.norm(c - b) + 1e-6
    )
    return np.degrees(np.arccos(np.clip(cos_val, -1.0, 1.0)))

def detect_touch_face(lms, w, h):
    try:
        nose = np.array([lms[mp_pose.PoseLandmark.NOSE.value].x * w,
                         lms[mp_pose.PoseLandmark.NOSE.value].y * h])
        lw   = np.array([lms[mp_pose.PoseLandmark.LEFT_WRIST.value].x * w,
                         lms[mp_pose.PoseLandmark.LEFT_WRIST.value].y * h])
        rw   = np.array([lms[mp_pose.PoseLandmark.RIGHT_WRIST.value].x * w,
                         lms[mp_pose.PoseLandmark.RIGHT_WRIST.value].y * h])
        thr = w * 0.15
        return (np.linalg.norm(lw - nose) < thr or
                np.linalg.norm(rw - nose) < thr)
    except:
        return False

def get_landmarks(lms, lm_ids, cam_w, cam_h):
    a = [lms[lm_ids[0].value].x * cam_w, lms[lm_ids[0].value].y * cam_h]
    b = [lms[lm_ids[1].value].x * cam_w, lms[lm_ids[1].value].y * cam_h]
    c = [lms[lm_ids[2].value].x * cam_w, lms[lm_ids[2].value].y * cam_h]
    return a, b, c
