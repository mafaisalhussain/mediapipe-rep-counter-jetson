import cv2
import numpy as np
import os
import time
import webbrowser
import mediapipe as mp

from config import (
    USER_NAME, MEME_DIR, EXERCISES, GOALS,
    PANEL_W, BAR_H, GREEN, BLACK, ACCENT,
    DASHBOARD_PORT, get_motivation
)
from pose_detector   import calc_angle, detect_touch_face, get_landmarks
from overlay         import (
    draw_side_panel, draw_meme_panel, draw_top_bar,
    draw_bottom_bar, draw_angle_label, draw_skeleton,
    draw_levelup_flash
)
from tempo           import TempoTracker
from gamification    import load_player, save_player, award_rep, update_streak, update_best, get_level
from session_log     import save_session
from dashboard       import start_dashboard

mp_pose = mp.solutions.pose

# ── memes ─────────────────────────────────────────────────────
def load_memes():
    memes = []
    for i in range(1, 6):
        for ext in ["jpg", "jpeg", "png"]:
            path = os.path.join(MEME_DIR, f"meme{i}.{ext}")
            if os.path.exists(path):
                img = cv2.imread(path)
                if img is not None:
                    memes.append(img)
                break
    print(f"  {len(memes)} memes loaded.\n")
    return memes

# ── menu ──────────────────────────────────────────────────────
def show_menu(player):
    level, _, _ = get_level(player["total_xp"])
    print("\n" + "="*46)
    print(f"  REP COUNTER  |  {USER_NAME}  [{level['name']}  {player['total_xp']} XP]")
    print(f"  Streak: {player['streak']} day(s)  |  Sessions: {player['total_sessions']}")
    print("="*46)
    for k, ex in EXERCISES.items():
        print(f"  {k}.  {ex['name']:<18} ~{ex['cal_per_rep']} kcal  {ex['xp_per_rep']} XP/rep")
    print("  D.  Open dashboard in browser")
    print("  Q.  Quit")
    print("="*46)
    return input("  Select: ").strip().lower()

# ── main counter loop ─────────────────────────────────────────
def run_counter(ex, memes, player):
    name        = ex["name"]
    lm_ids      = ex["landmarks"]
    up_ang      = ex["up_angle"]
    dn_ang      = ex["down_angle"]
    cal_per_rep = ex["cal_per_rep"]
    xp_per_rep  = ex["xp_per_rep"]

    reps            = 0
    sets            = 1
    sets_data       = []
    stage           = None
    total_cals      = 0.0
    motivation      = f"Ready {USER_NAME}? Let's go!"
    meme_img        = None
    meme_end        = 0
    meme_index      = 0
    reset_cooldown  = 0
    last_angle      = None
    levelup_until   = 0
    frame_count     = 0       # for frame skipping
    cached_lms      = None    # last processed landmarks

    tempo   = TempoTracker()

    level, next_lv, _ = get_level(player["total_xp"])

    cap  = cv2.VideoCapture(0)
    pose = mp_pose.Pose(
        min_detection_confidence=0.6,
        min_tracking_confidence=0.6
    )

    ret, frame = cap.read()
    if not ret:
        print("  Camera error.")
        return
    cam_h, cam_w = frame.shape[:2]
    canvas_w = PANEL_W + cam_w
    canvas_h = cam_h + 2 * BAR_H

    print(f"\n  {name} — touch face to save set — Q quit — D dashboard\n")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        now         = time.time()
        frame_count += 1
        canvas      = np.zeros((canvas_h, canvas_w, 3), dtype=np.uint8)

        # place camera feed (offset by top bar height)
        canvas[BAR_H: BAR_H + cam_h, PANEL_W: PANEL_W + cam_w] = frame

        # ── pose every 2nd frame ──────────────────────────────
        if frame_count % 2 == 0:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            res = pose.process(rgb)
            if res.pose_landmarks:
                cached_lms = res.pose_landmarks.landmark

        if cached_lms is not None:
            lms = cached_lms

            # face-touch → save set
            if now > reset_cooldown and detect_touch_face(lms, cam_w, cam_h):
                sets_data.append({"set": sets, "reps": reps})
                pb_broken = update_best(player, name, reps)
                update_streak(player)
                save_player(player)
                sets          += 1
                motivation     = f"Set {sets}! Rest up {USER_NAME}!"
                reset_cooldown = now + 3
                tempo.reset()
                if pb_broken:
                    motivation = f"NEW BEST! {reps} reps!"
                reps  = 0
                stage = None
                if memes:
                    meme_img   = memes[meme_index % len(memes)]
                    meme_end   = now + 4
                    meme_index += 1

            a, b, c    = get_landmarks(lms, lm_ids, cam_w, cam_h)
            last_angle = calc_angle(a, b, c)

            if last_angle > up_ang:
                stage = "up"
            if last_angle < dn_ang and stage == "up":
                stage       = "down"
                reps       += 1
                total_cals += cal_per_rep

                # tempo
                tempo.record_rep()

                # XP + gamification
                leveled_up, new_lv_name = award_rep(player, xp_per_rep)
                player["total_reps"] += 1
                save_player(player)
                level, next_lv, _ = get_level(player["total_xp"])

                if leveled_up:
                    levelup_until = now + 2.5
                    motivation = f"LEVEL UP! {new_lv_name}!"
                else:
                    msg = get_motivation(reps, USER_NAME)
                    if msg:
                        motivation = msg

                if reps in {8, 12, 15} and memes:
                    meme_img   = memes[meme_index % len(memes)]
                    meme_end   = now + 4
                    meme_index += 1

            draw_skeleton(canvas, lms, cam_w, cam_h, PANEL_W)
            draw_angle_label(canvas, b, last_angle, PANEL_W)

        # ── HUD ───────────────────────────────────────────────
        draw_top_bar(canvas, USER_NAME, name, sets,
                     level["name"], player["total_xp"])

        next_goal = next((g for g in GOALS if g > reps), GOALS[-1])

        if meme_img is not None and now < meme_end:
            draw_meme_panel(canvas, meme_img, meme_end - now)
        else:
            meme_img = None
            draw_side_panel(
                canvas, reps, sets, total_cals, stage,
                last_angle, USER_NAME, name, next_goal,
                level["name"], player["total_xp"],
                tempo.avg_pace
            )

        draw_bottom_bar(canvas, reps, motivation, tempo.label)

        if now < levelup_until:
            draw_levelup_flash(canvas, level["name"])

        cv2.imshow(f"{USER_NAME}  |  Rep Counter", canvas)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            # save final set if it has reps
            if reps > 0:
                sets_data.append({"set": sets, "reps": reps})
                update_best(player, name, reps)
            update_streak(player)
            save_player(player)
            save_session(name, sets_data, total_cals,
                         player["total_xp"], {**tempo.summary(), "label": tempo.label})
            print(f"\n  ── Session summary ──────────────────")
            print(f"  Exercise : {name}")
            print(f"  Sets     : {sets}")
            print(f"  Calories : {total_cals:.1f} kcal")
            print(f"  XP total : {player['total_xp']}")
            print(f"  Level    : {level['name']}")
            print(f"  ─────────────────────────────────────\n")
            break
        elif key == ord('d'):
            webbrowser.open(f"http://localhost:{DASHBOARD_PORT}")

    cap.release()
    cv2.destroyAllWindows()
    pose.close()

# ── entry ─────────────────────────────────────────────────────
if __name__ == "__main__":
    start_dashboard()
    memes  = load_memes()
    player = load_player()
    player["name"] = USER_NAME

    while True:
        choice = show_menu(player)
        if choice == "q":
            print(f"\n  Great work {USER_NAME}! See you next session.\n")
            break
        elif choice == "d":
            webbrowser.open(f"http://localhost:{DASHBOARD_PORT}")
        elif choice in EXERCISES:
            run_counter(EXERCISES[choice], memes, player)
            player = load_player()   # reload after session
        else:
            print("  Invalid choice, try again.")
