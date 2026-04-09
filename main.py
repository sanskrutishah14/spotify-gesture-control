import cv2
import mediapipe as mp
import time
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import math
from dotenv import load_dotenv
import os
load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope="user-modify-playback-state user-read-playback-state"
))

def get_active_device():
    devices = sp.devices()
    if devices['devices']:
        return devices['devices'][0]['id']
    return None

def play_music():
    device_id = get_active_device()
    if device_id:
        try:
            sp.start_playback(device_id=device_id)
        except Exception as e:
            print("Play error:", e)

def pause_music():
    device_id = get_active_device()
    if device_id:
        try:
            sp.pause_playback(device_id=device_id)
        except Exception as e:
            print("Pause error:", e)

def next_song():
    try:
        sp.next_track()
    except Exception as e:
        print("Next error:", e)

def prev_song():
    try:
        sp.previous_track()
    except Exception as e:
        print("Prev error:", e)

def set_volume(vol):
    try:
        vol = int(max(0, min(vol, 100)))
        sp.volume(vol)
    except:
        pass

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

last_action_time = 0
cooldown = 1.5
prev_x = None
prev_volume = 0

def is_fist(lm):
    return (
        lm[8].y > lm[6].y and
        lm[12].y > lm[10].y and
        lm[16].y > lm[14].y and
        lm[20].y > lm[18].y
    )

def is_palm(lm):
    return (
        lm[8].y < lm[6].y and
        lm[12].y < lm[10].y and
        lm[16].y < lm[14].y and
        lm[20].y < lm[18].y
    )

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1) 

    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            lm = handLms.landmark
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

            #SWIPE (ONE FINGER)
            x = lm[8].x

            if prev_x is not None:
                dx = x - prev_x

                if abs(dx) > 0.12 and time.time() - last_action_time > 1:
                    if dx > 0:
                        next_song()
                        print("Next 👉")
                    else:
                        prev_song()
                        print("Previous 👈")

                    last_action_time = time.time()

            prev_x = x

            #PLAY / PAUSE
            if time.time() - last_action_time > cooldown:

                if is_palm(lm):
                    play_music()
                    print("Play ✋")
                    last_action_time = time.time()

                elif is_fist(lm):
                    pause_music()
                    print("Pause ✊")
                    last_action_time = time.time()

            #FAST VOLUME CONTROL
            x1, y1 = int(lm[4].x * w), int(lm[4].y * h)
            x2, y2 = int(lm[8].x * w), int(lm[8].y * h)

            distance = math.hypot(x2 - x1, y2 - y1)

            volume = np.interp(distance, [20, 250], [0, 100])

            if abs(volume - prev_volume) > 5:
                set_volume(volume)
                prev_volume = volume

            cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 3)
            cv2.putText(frame, f'Volume: {int(volume)}%', (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            #LEGEND
            cv2.rectangle(frame, (10, 100), (300, 260), (0, 0, 0), -1)  # background box

            cv2.putText(frame, "Controls:", (20, 130),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            cv2.putText(frame, "Palm  -> Play", (20, 160),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            cv2.putText(frame, "Fist  -> Pause", (20, 185),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            cv2.putText(frame, "Swipe Right -> Next", (20, 210),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            cv2.putText(frame, "Swipe Left  -> Prev", (20, 235),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            cv2.putText(frame, "Pinch -> Volume", (20, 260),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    cv2.imshow("Gesture Spotify Control", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()