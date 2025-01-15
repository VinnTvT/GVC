import cv2
import mediapipe as mp
import pyautogui

x1 = y1 = x2 = y2 = 0

webcam = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

while True:
    success, image = webcam.read()
    if not success:
        break
    frame_height, frame_width = image.shape[:2]
    image = cv2.flip(image, 1)
    imgRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        handLms = results.multi_hand_landmarks[0]
        landmarks = handLms.landmark

        for id, lm in enumerate(landmarks):
            x = int(lm.x * frame_width)
            y = int(lm.y * frame_height)
            if id == 8:
                cv2.circle(img=image, center=(x, y), radius=8, color=(0, 255, 255), thickness=3)
                x1 = x
                y1 = y
            if id == 4:
                cv2.circle(img=image, center=(x, y), radius=8, color=(0, 255, 255), thickness=3)
                x2 = x
                y2 = y
                dist = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
                cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 5)
                if dist > 100:
                    pyautogui.press('volumeup')
                elif dist < 50:
                    pyautogui.press('volumedown')

        mpDraw.draw_landmarks(image, handLms, mpHands.HAND_CONNECTIONS)

    cv2.imshow("Hand Volume Gesture", image)
    key = cv2.waitKey(10)
    if key == 27:
        break

webcam.release()
cv2.destroyAllWindows()