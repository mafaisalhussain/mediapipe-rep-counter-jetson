import cv2
from pose_detector import PoseDetector
from rep_counter import RepCounter
from overlay import draw_overlay
from config import EXERCISES, DEFAULT_EXERCISE

def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    detector = PoseDetector()
    exercise_name = DEFAULT_EXERCISE
    exercise = EXERCISES[exercise_name]
    counter = RepCounter(
        up_thresh=exercise["up_thresh"],
        down_thresh=exercise["down_thresh"]
    )

    print(f"Starting rep counter | Exercise: {exercise_name}")
    print("Press 'q' to quit | Press 'r' to reset count | Press 'e' to switch exercise")

    exercise_keys = list(EXERCISES.keys())
    exercise_idx = exercise_keys.index(exercise_name)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Camera not found. Check /dev/video0")
            break

        frame = detector.find_pose(frame, draw=True)

        angle = None
        if detector.results and detector.results.pose_landmarks:
            try:
                landmarks = detector.results.pose_landmarks.landmark
                a = detector.get_landmark(frame, exercise["points"][0])
                b = detector.get_landmark(frame, exercise["points"][1])
                c = detector.get_landmark(frame, exercise["points"][2])
                angle = detector.compute_angle(a, b, c)
                reps, feedback = counter.update(angle)
            except Exception:
                reps = counter.count
                feedback = counter.feedback
        else:
            reps = counter.count
            feedback = "No pose detected"

        frame = draw_overlay(frame, reps, angle, feedback, exercise_name, counter.state)
        cv2.imshow("Rep Counter - Jetson Nano", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r'):
            counter.reset()
            print("Rep count reset.")
        elif key == ord('e'):
            exercise_idx = (exercise_idx + 1) % len(exercise_keys)
            exercise_name = exercise_keys[exercise_idx]
            exercise = EXERCISES[exercise_name]
            counter = RepCounter(
                up_thresh=exercise["up_thresh"],
                down_thresh=exercise["down_thresh"]
            )
            print(f"Switched to: {exercise_name}")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
