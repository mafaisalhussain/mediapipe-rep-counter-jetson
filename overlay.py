import cv2
import numpy as np
from config import (
    PANEL_W, BAR_H, ACCENT, GREEN, CYAN, YELLOW,
    WHITE, GRAY, BLACK, ORANGE, RED, GOALS, LEVELS
)

def put_text(canvas, text, pos, scale, color, thickness=1):
    cv2.putText(canvas, str(text), pos,
                cv2.FONT_HERSHEY_SIMPLEX, scale, color, thickness, cv2.LINE_AA)

def _progress_bar(canvas, x, y, w, h, pct, color):
    cv2.rectangle(canvas, (x, y), (x + w, y + h), (40, 40, 40), -1)
    fill = int(w * min(max(pct, 0), 1))
    if fill > 0:
        cv2.rectangle(canvas, (x, y), (x + fill, y + h), color, -1)
    cv2.rectangle(canvas, (x, y), (x + w, y + h), GRAY, 1)

def draw_top_bar(canvas, name, exercise, sets, level_name, total_xp):
    h, w = canvas.shape[:2]
    cv2.rectangle(canvas, (0, 0), (w, BAR_H), (18, 18, 28), -1)
    cv2.line(canvas, (0, BAR_H), (w, BAR_H), ACCENT, 1)
    put_text(canvas, f"{name}  |  {exercise}", (10, 24), 0.5, WHITE, 1)
    lv_text = f"SET {sets}  |  {level_name}  {total_xp} XP"
    (tw, _), _ = cv2.getTextSize(lv_text, cv2.FONT_HERSHEY_SIMPLEX, 0.42, 1)
    put_text(canvas, lv_text, (w - tw - 10, 24), 0.42, ACCENT, 1)

def draw_bottom_bar(canvas, reps, motivation, tempo_label=""):
    h, fw = canvas.shape[:2]
    cv2.rectangle(canvas, (0, h - BAR_H), (fw, h), (18, 18, 28), -1)
    cv2.line(canvas, (0, h - BAR_H), (fw, h - BAR_H), ACCENT, 1)

    # rep badge
    badge_text = str(reps)
    (bw, bh), _ = cv2.getTextSize(badge_text, cv2.FONT_HERSHEY_SIMPLEX, 0.65, 2)
    cv2.rectangle(canvas, (8, h - BAR_H + 4), (8 + bw + 10, h - 4), GREEN, -1)
    put_text(canvas, badge_text, (13, h - 9), 0.65, BLACK, 2)

    put_text(canvas, motivation, (bw + 28, h - 10), 0.44, WHITE, 1)

    # tempo label
    if tempo_label:
        color = {"fast": RED, "steady": GREEN, "slow": YELLOW}.get(tempo_label, GRAY)
        (tw, _), _ = cv2.getTextSize(tempo_label, cv2.FONT_HERSHEY_SIMPLEX, 0.38, 1)
        put_text(canvas, tempo_label, (fw - tw - 60, h - 10), 0.38, color, 1)

    # D key hint
    hint = "[D] stats"
    (hw, _), _ = cv2.getTextSize(hint, cv2.FONT_HERSHEY_SIMPLEX, 0.32, 1)
    put_text(canvas, hint, (fw - hw - 8, h - 10), 0.32, GRAY, 1)

def draw_side_panel(canvas, reps, sets, total_cals, stage,
                    angle, name, exercise, next_goal,
                    level_name, total_xp, tempo_avg):
    h = canvas.shape[0]
    cv2.rectangle(canvas, (0, BAR_H), (PANEL_W, h - BAR_H), (14, 17, 23), -1)
    cv2.line(canvas, (PANEL_W, BAR_H), (PANEL_W, h - BAR_H), ACCENT, 1)

    y = BAR_H + 22
    def row(label, val, vcol=WHITE):
        nonlocal y
        put_text(canvas, label, (10, y), 0.36, GRAY)
        put_text(canvas, str(val), (10, y + 18), 0.52, vcol, 1)
        y += 46

    # big rep count
    put_text(canvas, str(reps), (12, y + 28), 1.6, GREEN, 3)
    put_text(canvas, "reps", (12, y + 58), 0.42, GRAY)
    y += 78

    # progress bar toward next goal
    pct = reps / next_goal if next_goal else 0
    _progress_bar(canvas, 10, y, PANEL_W - 20, 7, pct, ACCENT)
    put_text(canvas, f"goal {next_goal}", (10, y + 20), 0.34, GRAY)
    y += 32

    row("SET",      sets,                     CYAN)
    row("CALS",     f"{total_cals:.1f}",      ORANGE)
    row("STAGE",    stage or "—",             YELLOW if stage == "up" else WHITE)
    row("ANGLE",    f"{int(angle)}°" if angle else "—", YELLOW)

    # level + XP mini bar
    put_text(canvas, level_name, (10, y), 0.38, ACCENT)
    y += 16
    # find xp range for current level
    idx = next((i for i,lv in enumerate(LEVELS) if lv["name"]==level_name), 0)
    cur_min = LEVELS[idx]["min_xp"]
    nxt_min = LEVELS[idx+1]["min_xp"] if idx+1 < len(LEVELS) else cur_min + 500
    pct_xp  = (total_xp - cur_min) / max(nxt_min - cur_min, 1)
    _progress_bar(canvas, 10, y, PANEL_W - 20, 5, pct_xp, ACCENT)
    put_text(canvas, f"{total_xp} XP", (10, y + 18), 0.34, GRAY)
    y += 28

    # tempo avg
    if tempo_avg:
        put_text(canvas, f"pace {tempo_avg:.1f}s/rep", (10, y), 0.34, GRAY)

def draw_meme_panel(canvas, meme_img, countdown):
    h = canvas.shape[0]
    panel_h = h - 2 * BAR_H
    meme = cv2.resize(meme_img, (PANEL_W, panel_h))
    canvas[BAR_H: h - BAR_H, 0: PANEL_W] = meme
    # countdown bar
    pct = countdown / 4.0
    bar_w = int(PANEL_W * pct)
    cv2.rectangle(canvas, (0, h - BAR_H - 5), (bar_w, h - BAR_H), GREEN, -1)

def draw_skeleton(canvas, lms, cam_w, cam_h, panel_w):
    import mediapipe as mp
    for conn in mp.solutions.pose.POSE_CONNECTIONS:
        s, e = conn
        sx = int(lms[s].x * cam_w) + panel_w
        sy = int(lms[s].y * cam_h) + BAR_H
        ex = int(lms[e].x * cam_w) + panel_w
        ey = int(lms[e].y * cam_h) + BAR_H
        cv2.line(canvas, (sx, sy), (ex, ey), (180, 180, 180), 1, cv2.LINE_AA)
    for lm in lms:
        px = int(lm.x * cam_w) + panel_w
        py = int(lm.y * cam_h) + BAR_H
        cv2.circle(canvas, (px, py), 4, (220, 80, 80), -1, cv2.LINE_AA)

def draw_angle_label(canvas, b, angle, panel_w):
    jx = int(b[0]) + panel_w
    jy = int(b[1]) + BAR_H
    label = f"{int(angle)}"
    (lw, lh), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 1)
    cv2.rectangle(canvas, (jx - lw//2 - 4, jy - lh - 8),
                           (jx + lw//2 + 4, jy + 2), BLACK, -1)
    cv2.rectangle(canvas, (jx - lw//2 - 4, jy - lh - 8),
                           (jx + lw//2 + 4, jy + 2), YELLOW, 1)
    put_text(canvas, label, (jx - lw//2, jy - 2), 0.55, YELLOW, 1)

def draw_levelup_flash(canvas, level_name):
    h, w = canvas.shape[:2]
    overlay = canvas.copy()
    cv2.rectangle(overlay, (0, 0), (w, h), (50, 30, 120), -1)
    cv2.addWeighted(overlay, 0.35, canvas, 0.65, 0, canvas)
    msg = f"LEVEL UP!  {level_name}"
    (tw, th), _ = cv2.getTextSize(msg, cv2.FONT_HERSHEY_SIMPLEX, 1.0, 2)
    cx, cy = (w - tw) // 2, h // 2
    put_text(canvas, msg, (cx, cy), 1.0, (180, 140, 255), 2)
