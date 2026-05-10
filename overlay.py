import cv2
import numpy as np
from config import (
    PANEL_W, BAR_H, ACCENT, GREEN, CYAN,
    YELLOW, WHITE, GRAY, BLACK
)

def put_text(img, text, pos, scale, color, thick=1, anchor="left"):
    font = cv2.FONT_HERSHEY_SIMPLEX
    if anchor == "center":
        (tw, _), _ = cv2.getTextSize(text, font, scale, thick)
        pos = (pos[0] - tw // 2, pos[1])
    cv2.putText(img, text, pos, font, scale, color, thick, cv2.LINE_AA)

def draw_rect_alpha(img, pt1, pt2, color, alpha=0.85):
    overlay = img.copy()
    cv2.rectangle(overlay, pt1, pt2, color, -1)
    cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)

def progress_bar(img, x, y, w, h, value, max_val, color):
    cv2.rectangle(img, (x, y), (x + w, y + h), (50, 50, 50), -1)
    fill = int((min(value, max_val) / max_val) * w)
    if fill > 0:
        cv2.rectangle(img, (x, y), (x + fill, y + h), color, -1)
    cv2.rectangle(img, (x, y), (x + w, y + h), (80, 80, 80), 1)

def draw_side_panel(canvas, reps, sets, total_cals, stage, angle, user_name, ex_name, next_goal):
    h = canvas.shape[0]
    w = PANEL_W

    draw_rect_alpha(canvas, (0, BAR_H), (w, h - BAR_H), (15, 15, 15), 0.95)
    cv2.rectangle(canvas, (0, BAR_H), (3, h - BAR_H), ACCENT, -1)
    cv2.line(canvas, (w, BAR_H), (w, h - BAR_H), (50, 50, 50), 1)

    cy = BAR_H + 28
    put_text(canvas, user_name.upper(), (w // 2, cy), 0.42, ACCENT, 1, "center")
    cy += 14
    cv2.line(canvas, (10, cy), (w - 10, cy), (50, 50, 50), 1)
    cy += 16
    put_text(canvas, ex_name, (w // 2, cy), 0.38, GRAY, 1, "center")
    cy += 22
    cv2.line(canvas, (10, cy), (w - 10, cy), (40, 40, 40), 1)
    cy += 20

    put_text(canvas, str(reps), (w // 2, cy + 30), 1.6, GREEN, 3, "center")
    cy += 44
    put_text(canvas, "REPS", (w // 2, cy), 0.35, GRAY, 1, "center")
    cy += 20

    cv2.line(canvas, (10, cy), (w - 10, cy), (40, 40, 40), 1)
    cy += 10
    put_text(canvas, f"Goal: {next_goal} reps", (w // 2, cy), 0.32, GRAY, 1, "center")
    cy += 8
    progress_bar(canvas, 10, cy, w - 20, 6, reps, next_goal, ACCENT)
    cy += 20

    cv2.line(canvas, (10, cy), (w - 10, cy), (40, 40, 40), 1)
    cy += 16

    put_text(canvas, "SETS",  (14, cy), 0.33, GRAY, 1)
    put_text(canvas, str(sets), (w - 10, cy), 0.38, WHITE, 1)
    cy += 18

    put_text(canvas, "CALS",  (14, cy), 0.33, GRAY, 1)
    put_text(canvas, f"{total_cals:.1f}", (w - 10, cy), 0.38, (100, 180, 255), 1)
    cy += 18

    put_text(canvas, "STAGE", (14, cy), 0.33, GRAY, 1)
    stage_col = GREEN if stage == "down" else CYAN
    put_text(canvas, (stage or "-").upper(), (w - 10, cy), 0.35, stage_col, 1)
    cy += 18

    put_text(canvas, "ANGLE", (14, cy), 0.33, GRAY, 1)
    angle_str = f"{int(angle)}" if angle is not None else "-"
    put_text(canvas, angle_str, (w - 10, cy), 0.35, YELLOW, 1)
    cy += 22

    cv2.line(canvas, (10, cy), (w - 10, cy), (40, 40, 40), 1)
    cy += 14
    put_text(canvas, "Touch face", (w // 2, cy), 0.28, (80, 80, 80), 1, "center")
    cy += 12
    put_text(canvas, "= new set",  (w // 2, cy), 0.28, (80, 80, 80), 1, "center")

def draw_meme_panel(canvas, meme, countdown):
    h = canvas.shape[0]
    panel_h = h - BAR_H * 2
    resized = cv2.resize(meme, (PANEL_W, panel_h))
    canvas[BAR_H: h - BAR_H, 0: PANEL_W] = resized
    bar_y = h - BAR_H - 18
    draw_rect_alpha(canvas, (0, bar_y), (PANEL_W, bar_y + 18), BLACK, 0.7)
    progress_bar(canvas, 4, bar_y + 6, PANEL_W - 8, 6, countdown, 4.0, ACCENT)
    cv2.rectangle(canvas, (0, BAR_H), (3, h - BAR_H), ACCENT, -1)
    cv2.line(canvas, (PANEL_W, BAR_H), (PANEL_W, h - BAR_H), (50, 50, 50), 1)

def draw_top_bar(canvas, user_name, ex_name, sets):
    fw = canvas.shape[1]
    draw_rect_alpha(canvas, (0, 0), (fw, BAR_H), BLACK, 0.88)
    cv2.rectangle(canvas, (0, 0), (4, BAR_H), ACCENT, -1)
    put_text(canvas, user_name.upper(), (16, 23), 0.52, WHITE, 1)
    put_text(canvas, f"  |  {ex_name}", (16 + len(user_name) * 9, 23), 0.42, GRAY, 1)
    badge_text = f"SET {sets}"
    (bw, _), _ = cv2.getTextSize(badge_text, cv2.FONT_HERSHEY_SIMPLEX, 0.38, 1)
    bx = fw - bw - 24
    cv2.rectangle(canvas, (bx - 8, 8), (fw - 10, BAR_H - 8), ACCENT, -1)
    put_text(canvas, badge_text, (bx, 24), 0.38, WHITE, 1)
    cv2.line(canvas, (0, BAR_H), (fw, BAR_H), (60, 60, 60), 1)

def draw_bottom_bar(canvas, reps, motivation):
    h, fw = canvas.shape[:2]
    y = h - BAR_H
    draw_rect_alpha(canvas, (0, y), (fw, h), BLACK, 0.88)
    cv2.rectangle(canvas, (0, y), (4, h), GREEN, -1)
    cv2.line(canvas, (0, y), (fw, y), (60, 60, 60), 1)
    badge_w = 52
    cv2.rectangle(canvas, (8, y + 5), (8 + badge_w, h - 5), GREEN, -1)
    put_text(canvas, str(reps), (8 + badge_w // 2, h - 8), 0.7, BLACK, 2, "center")
    cv2.line(canvas, (8 + badge_w + 6, y + 6), (8 + badge_w + 6, h - 6), (60, 60, 60), 1)
    put_text(canvas, motivation, (8 + badge_w + 16, h - 10), 0.46, WHITE, 1)
    hint = "Q = menu"
    (hw, _), _ = cv2.getTextSize(hint, cv2.FONT_HERSHEY_SIMPLEX, 0.32, 1)
    put_text(canvas, hint, (fw - hw - 12, h - 10), 0.32, GRAY, 1)

def draw_angle_label(canvas, b, angle, panel_w, bar_h):
    jx = int(b[0]) + panel_w
    jy = int(b[1]) + bar_h
    label = f"{int(angle)}"
    (lw, lh), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 1)
    cv2.rectangle(canvas, (jx - lw // 2 - 4, jy - lh - 8),
                           (jx + lw // 2 + 4, jy + 2), BLACK, -1)
    cv2.rectangle(canvas, (jx - lw // 2 - 4, jy - lh - 8),
                           (jx + lw // 2 + 4, jy + 2), YELLOW, 1)
    put_text(canvas, label, (jx - lw // 2, jy - 2), 0.55, YELLOW, 1)

def draw_skeleton(canvas, lms, cam_w, cam_h, panel_w):
    import mediapipe as mp
    mp_pose = mp.solutions.pose
    for connection in mp_pose.POSE_CONNECTIONS:
        s, e = connection
        sx = int(lms[s].x * cam_w) + panel_w
        sy = int(lms[s].y * cam_h)
        ex = int(lms[e].x * cam_w) + panel_w
        ey = int(lms[e].y * cam_h)
        cv2.line(canvas, (sx, sy), (ex, ey), (200, 200, 200), 1, cv2.LINE_AA)
    for lm in lms:
        px = int(lm.x * cam_w) + panel_w
        py = int(lm.y * cam_h)
        cv2.circle(canvas, (px, py), 4, (220, 80, 80), -1, cv2.LINE_AA)
