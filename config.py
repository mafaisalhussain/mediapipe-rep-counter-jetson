import mediapipe as mp

mp_pose = mp.solutions.pose
L = mp_pose.PoseLandmark

# Each exercise defines:
#   points     : 3 landmark indices (A, B, C) where B is the joint vertex
#   up_thresh  : angle considered "extended / up"
#   down_thresh: angle considered "contracted / down"

EXERCISES = {
    "Bicep Curl": {
        "points": [L.LEFT_SHOULDER.value, L.LEFT_ELBOW.value, L.LEFT_WRIST.value],
        "up_thresh":   160,
        "down_thresh":  50,
    },
    "Push Up": {
        "points": [L.LEFT_SHOULDER.value, L.LEFT_ELBOW.value, L.LEFT_WRIST.value],
        "up_thresh":   160,
        "down_thresh":  70,
    },
    "Squat": {
        "points": [L.LEFT_HIP.value, L.LEFT_KNEE.value, L.LEFT_ANKLE.value],
        "up_thresh":   170,
        "down_thresh":  90,
    },
}

DEFAULT_EXERCISE = "Bicep Curl"
