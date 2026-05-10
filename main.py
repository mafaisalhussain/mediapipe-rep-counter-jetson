import cv2
import numpy as np
import os
import time
import mediapipe as mp

from config import (
    USER_NAME, MEME_DIR, EXERCISES, GOALS,
    PANEL_W, BAR_H, GREEN, BLACK, ACCENT,
    get_motivation
)
from pose_detector import calc_angle, detect_touch_face, get_landmarks
from overlay import (
    draw_side_panel, draw_meme_panel, draw_top_bar,
    draw_bottom_bar, draw_angle_label, draw_skeleton
)

mp_pose = mp.solutions.pose

# ── load memes ────────────────────────────────────────────────
def load_memes():
    memes = []
    for i in range(1, 6):
        for ext in ["jpg", "jpeg", "png"]:
            path = os.path.join(MEME_DIR, f"meme{i}.{ext}")
            if os.path.exists(path):
                img = cv2.imread(path)
                if img is not None:
                    memes.append(img)
                    print(f"  loaded: meme{i}.{ext}")
                break
    print(f"  {len(memes)} memes ready.\n")
    return memes

# ── menu ──────────────────────────────────────────────────────
def show_menu():
    print("\n" + "="*46)
    print(f"      REP COUNTER  |  Welcome, {USER_NAME}!")
    print("="*46)
    for k, ex in EXERCISES.items():
        print(f"  {k}.  {ex['name']:<18} ~{ex['cal_per_rep']} kcal/rep")
    print("  Q.  Quit")
    print("="*46)
    print("  [Touch face to save set & reset reps]")
    print("="*46)
    return input("  Select: ").strip().lower()

# ── counter ───────────────────────────────────────────────────
def run_counter(ex, memes):
    name        = ex["name"]
    lm_ids      = ex["landmarks"]
    up_ang      = ex["up_angle"]
    dn_ang      = ex["down_angle"]
    cal_per_rep = ex["cal_per_rep"]

    reps           = 0
    sets           = 1
    stage          = None
    total_cals     = 0.0
    motivation     = f"Ready {USER_NAME}? Let's go!"
    meme_img       = None
    meme_end       = 0
    meme_index     = 0
    reset_cooldown = 0
    last_angle     = None

    cap  = cv2.VideoCapture(0)
    pose = mp_pose.Pose(
        min_detection_confidence=0.6,
        min_tracking_confidence=0.6
    )

    ret, frame = cap.read()
    if not ret:
        print("Camera error.")
        return
    cam_h, cam_w = frame.shape[:2]
    canvas_w = PANEL_W + cam_w
    canvas_h = cam_h

    print(f"\n  {name} started — touch face to save set — Q to quit\n")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        now    = time.time()
        rgb    = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        res    = pose.process(rgb)
        canvas = np.zeros((canvas_h, canvas_w, 3), dtype=np.uint8)
        canvas[0:cam_h, PANEL_W:PANEL_W + cam_w] = frame

        if res.pose_landmarks:
            lms = res.pose_landmarks.landmark

            if now > reset_cooldown and detect_touch_face(lms, cam_w, cam_h):
                sets          += 1
                reps           = 0
                stage          = None
                motivation     = f"Set {sets}! Rest up {USER_NAME}!"
                reset_cooldown = now + 3
                if memes:
                    meme_img   = memes[meme_index % len(memes)]
                    meme_end   = now + 2
                    meme_index += 1
                print(f"  Set {sets} saved. Reps reset.")

            a, b, c    = get_landmarks(lms, lm_ids, cam_w, cam_h)
            last_angle = calc_angle(a, b, c)

            if last_angle > up_ang:
                stage = "up"
            if last_angle < dn_ang and stage == "up":
                stage       = "down"
                reps       += 1
                total_cals += cal_per_rep
                msg = get_motivation(reps, USER_NAME)
                if msg:
                    motivation = msg
                if reps in {8, 12, 15} and memes:
                    meme_img   = memes[meme_index % len(memes)]
                    meme_end   = now + 4
                    meme_index += 1

            draw_skeleton(canvas, lms, cam_w, cam_h, PANEL_W)
            draw_angle_label(canvas, b, last_angle, PANEL_W, BAR_H)

        draw_top_bar(canvas, USER_NAME, name, sets)

        next_goal = next((g for g in GOALS if g > reps), GOALS[-1])
        if meme_img is not None and now < meme_end:
            draw_meme_panel(canvas, meme_img, meme_end - now)
        else:
            meme_img = None
            draw_side_panel(canvas, reps, sets, total_cals,
                            stage, last_angle, USER_NAME, name, next_goal)

        draw_bottom_bar(canvas, reps, motivation)

        cv2.imshow(f"{USER_NAME} Rep Counter", canvas)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print(f"\n  ── Session Summary ──────────────────")
            print(f"  Exercise  : {name}")
            print(f"  Sets done : {sets - 1}")
            print(f"  Last set  : {reps} reps")
            print(f"  Calories  : {total_cals:.1f} kcal")
            print(f"  ─────────────────────────────────────\n")
            break

    cap.release()
    cv2.destroyAllWindows()
    pose.close()

# ── entry ─────────────────────────────────────────────────────
if __name__ == "__main__":
    memes = load_memes()
    while True:
        choice = show_menu()
        if choice == "q":
            print(f"\n  Great work {USER_NAME}! See you next session.\n")
            break
        elif choice in EXERCISES:
            run_counter(EXERCISES[choice], memes)
        else:
            print("  Invalid choice, try again.")
