from collections import deque
import time

import cv2
import mediapipe as mp
import numpy as np
import pyautogui

from helpers import fingers_state, pinch_dist

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

screen_w, screen_h = pyautogui.size()

postion_buffer = deque(maxlen=4)
ema_alpha = 0.4
ema_x, ema_y = None, None

last_click_time = 0
click_cooldown = 0.5

while True:
    _, frame = cap.read()

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    h, w, _ = frame.shape

    results = hands.process(rgb_frame)
    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        lms = hand.landmark

        ix, iy = int(lms[8].x * w), int(lms[8].y * h)
        tx, ty = int(lms[4].x * w), int(lms[4].y * h)
        mx, my = int(lms[12].x * w), int(lms[12].y * h)

        # Track Index
        screen_x = np.interp(ix, (0, w * 2), (0, screen_w * 2))
        screen_y = np.interp(iy, (0, h), (0, screen_h))
        postion_buffer.append((screen_x, screen_y))
        avg_x = np.mean([pt[0] for pt in postion_buffer])
        avg_y = np.mean([pt[1] for pt in postion_buffer])
        if not ema_x:
            ema_x, ema_y = avg_x, avg_y
        else:
            ema_x = ema_alpha * avg_x + (1 - ema_alpha) * ema_x
            ema_y = ema_alpha * avg_y + (1 - ema_alpha) * ema_y
        pyautogui.moveTo(ema_x, ema_y, duration=0.01)

        # Click
        click_pinch_dist = pinch_dist(ix, tx, iy, ty)
        if click_pinch_dist < 30 and (time.time() - last_click_time > click_cooldown):
            pyautogui.click()
            last_click_time = time.time()
            cv2.putText(frame, 'Click!', (ix + 20, iy - 20), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 0, 255), 2)

        # Right Click
        right_click = pinch_dist(mx, tx, my, ty)
        if right_click < 20 and (time.time() - last_click_time > click_cooldown):
            pyautogui.rightClick()
            last_click_time = time.time()
            cv2.putText(frame, 'Right Click!', (ix + 20, iy - 20), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 0, 255), 2)

        # Scroll
        fingers = fingers_state(lms)
        if all(fingers):
            pyautogui.scroll(30)
        elif not any(fingers):
            pyautogui.scroll(-30)

        cv2.circle(frame, (ix, iy), 10, (0, 0, 255), -1)
        cv2.circle(frame, (tx, ty), 10, (0, 0, 255), -1)
        cv2.circle(frame, (mx, my), 10, (0, 0, 255), -1)
        cv2.line(frame, (ix, iy), (tx, ty), (255, 255, 255), 2)
        mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

    cv2.imshow('Hand Tracking', frame)
    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()
