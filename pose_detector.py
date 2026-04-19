import cv2
import mediapipe as mp
import numpy as np

class PoseDetector:
    def __init__(self, detection_conf=0.7, tracking_conf=0.7):
        self.mp_pose = mp.solutions.pose
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=detection_conf,
            min_tracking_confidence=tracking_conf
        )
        self.results = None

    def find_pose(self, frame, draw=True):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb.flags.writeable = False
        self.results = self.pose.process(rgb)
        rgb.flags.writeable = True

        if self.results.pose_landmarks and draw:
            self.mp_draw.draw_landmarks(
                frame,
                self.results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style()
            )
        return frame

    def get_landmark(self, frame, idx):
        h, w = frame.shape[:2]
        lm = self.results.pose_landmarks.landmark[idx]
        return int(lm.x * w), int(lm.y * h)

    def compute_angle(self, a, b, c):
        a = np.array(a, dtype=float)
        b = np.array(b, dtype=float)
        c = np.array(c, dtype=float)
        ba = a - b
        bc = c - b
        norm = np.linalg.norm(ba) * np.linalg.norm(bc)
        if norm == 0:
            return 0.0
        cos_angle = np.dot(ba, bc) / norm
        cos_angle = np.clip(cos_angle, -1.0, 1.0)
        return float(np.degrees(np.arccos(cos_angle)))
