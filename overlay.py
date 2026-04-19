import cv2

# Colors (BGR)
WHITE   = (255, 255, 255)
BLACK   = (0,   0,   0)
GREEN   = (0,   200, 100)
BLUE    = (255, 140, 0)
RED     = (0,   60,  220)
GRAY    = (180, 180, 180)
DARK    = (30,  30,  30)

def draw_rounded_rect(frame, x, y, w, h, r, color, alpha=0.6):
    overlay = frame.copy()
    cv2.rectangle(overlay, (x + r, y), (x + w - r, y + h), color, -1)
    cv2.rectangle(overlay, (x, y + r), (x + w, y + h - r), color, -1)
    for cx, cy in [(x+r, y+r), (x+w-r, y+r), (x+r, y+h-r), (x+w-r, y+h-r)]:
        cv2.circle(overlay, (cx, cy), r, color, -1)
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

def draw_overlay(frame, reps, angle, feedback, exercise_name, state):
    h, w = frame.shape[:2]

    # Rep count panel (top left)
    draw_rounded_rect(frame, 10, 10, 200, 110, 12, DARK, alpha=0.65)
    cv2.putText(frame, exercise_name.upper(), (22, 38),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, GRAY, 1, cv2.LINE_AA)
    cv2.putText(frame, str(reps), (22, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 2.8, GREEN, 4, cv2.LINE_AA)
    cv2.putText(frame, "REPS", (110, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, GRAY, 1, cv2.LINE_AA)

    # Angle display (top right)
    if angle is not None:
        angle_text = f"{int(angle)}"
        draw_rounded_rect(frame, w - 130, 10, 120, 70, 12, DARK, alpha=0.65)
        cv2.putText(frame, "ANGLE", (w - 118, 34),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, GRAY, 1, cv2.LINE_AA)
        cv2.putText(frame, angle_text + u"\u00b0", (w - 118, 68),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.1, BLUE, 2, cv2.LINE_AA)

    # Feedback bar (bottom)
    bar_h = 54
    draw_rounded_rect(frame, 0, h - bar_h, w, bar_h, 0, DARK, alpha=0.7)

    state_color = GREEN if state == "up" else RED if state == "down" else GRAY
    cv2.circle(frame, (28, h - bar_h + 27), 10, state_color, -1)

    cv2.putText(frame, feedback, (50, h - bar_h + 34),
                cv2.FONT_HERSHEY_SIMPLEX, 0.85, WHITE, 2, cv2.LINE_AA)

    # Controls hint
    cv2.putText(frame, "Q: quit   R: reset   E: switch exercise",
                (w - 360, h - bar_h + 34),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, GRAY, 1, cv2.LINE_AA)

    return frame
