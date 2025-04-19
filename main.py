import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import time
import math

# Disable pyautogui fail-safe
pyautogui.FAILSAFE = False

# Initialize MediaPipe Hands with optimized settings
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.3,  # Reduced for speed
    min_tracking_confidence=0.2     # Reduced for speed
)

# Get screen dimensions
screen_width, screen_height = pyautogui.size()

# Initialize OpenCV video capture with lower resolution
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)  # Lower resolution for faster processing
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
cap.set(cv2.CAP_PROP_FPS, 120)          # Try to get highest possible FPS

# Mouse control parameters
smoothing = 5  # Adjust smoothing factor for mouse movement
mouse_x, mouse_y = screen_width / 2, screen_height / 2
frame_scale = 3  # Scale factor from processed frame to display

# Gesture control
click_cooldown = 0
last_scroll_time = 0

# Performance optimizations
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

def get_landmark_coords(landmarks, landmark_id):
    return [landmarks.landmark[landmark_id].x, landmarks.landmark[landmark_id].y]

def calculate_distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

def fingers_up(landmarks):
    fingers = []
    # Thumb (horizontal comparison)
    fingers.append(1 if landmarks.landmark[4].x < landmarks.landmark[3].x else 0)
    # Other fingers (vertical comparison)
    for tip, pip in [(8, 6), (12, 10), (16, 14), (20, 18)]:
        fingers.append(1 if landmarks.landmark[tip].y < landmarks.landmark[pip].y else 0)
    return fingers

def process_gesture(landmarks, frame):
    global click_cooldown, mouse_x, mouse_y, last_scroll_time

    h, w = frame.shape[:2]
    fingers = fingers_up(landmarks)

    # Mouse movement (index finger only)
    if fingers[1] and not fingers[0]:
        index_tip = get_landmark_coords(landmarks, mp_hands.HandLandmark.INDEX_FINGER_TIP)
        target_x = np.interp(index_tip[0], [0.1, 0.9], [0, screen_width])
        target_y = np.interp(index_tip[1], [0.1, 0.9], [0, screen_height])
        mouse_x = mouse_x + (target_x - mouse_x) / smoothing
        mouse_y = mouse_y + (target_y - mouse_y) / smoothing
        pyautogui.moveTo(mouse_x, mouse_y)

    # Left click (thumb-index pinch)
    if click_cooldown <= 0 and calculate_distance(
            get_landmark_coords(landmarks, 4),
            get_landmark_coords(landmarks, 8)
    ) < 0.05:
        pyautogui.click()
        click_cooldown = 8

    # Right click (index-middle pinch)
    if click_cooldown <= 0 and calculate_distance(
            get_landmark_coords(landmarks, 8),
            get_landmark_coords(landmarks, 12)
    ) < 0.05:
        pyautogui.rightClick()
        click_cooldown = 8

    # Scrolling (open hand vertical movement)
    if sum(fingers) == 5 and time.time() - last_scroll_time > 0.1:
        palm_y = landmarks.landmark[0].y
        scroll_amount = int((0.5 - palm_y) * 500)
        pyautogui.scroll(scroll_amount)
        last_scroll_time = time.time()

    if click_cooldown > 0:
        click_cooldown -= 1

    return frame

# Main optimized loop
while cap.isOpened():
    # Capture frame
    success, frame = cap.read()
    if not success:
        continue

    # Mirror and resize frame
    frame = cv2.flip(frame, 1)
    processed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process hands
    results = hands.process(processed_frame)

    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            process_gesture(landmarks, frame)

            # Fast landmark drawing
            mp_drawing.draw_landmarks(
                frame,
                landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style()
            )

    # Display frame
    cv2.imshow('Hand Tracking', cv2.resize(frame,
                 (frame.shape[1] * frame_scale, frame.shape[0] * frame_scale)))

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
