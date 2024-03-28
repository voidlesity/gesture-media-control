# Tried to run pure mediapipe but it wasnt so easy setting up more gestures

from pynput.keyboard import Key, Controller
import mediapipe as mp
import cv2

# Constants
SWIPE_THRESHOLD = 200
RESET_DELAY_FRAMES = 10

# Initialize keyboard control and Mediapipe hands tracking
keyboard = Controller()
hands = mp.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=0.25)

# Start webcam capture
cap = cv2.VideoCapture(2)  
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)  
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

def leftSwipeFunction():
    keyboard.touch(Key.media_previous, True)
    print("Left Swipe Detected!")

def rightSwipeFunction():
    keyboard.touch(Key.media_next, True)
    print("Right Swipe Detected!")

# Main program loop
previousX = None
handDetected = False
delayCounter = 0

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Mediapipe processing
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    if results.multi_hand_landmarks:
        handDetected = True
        for handLandmarks in results.multi_hand_landmarks:
            indexFingerTip = handLandmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]
            currentX = int(indexFingerTip.x * frame.shape[1])

            # swipe gestures
            if previousX is not None:
                if abs(currentX - previousX) > SWIPE_THRESHOLD:
                    print("Difference:", abs(currentX - previousX))
                    if currentX > previousX:
                        leftSwipeFunction()
                    else:
                        rightSwipeFunction()
            previousX = currentX

            mp.solutions.drawing_utils.draw_landmarks(frame, handLandmarks, mp.solutions.hands.HAND_CONNECTIONS)
    else:
        handDetected = False
        if previousX is not None:
            delayCounter += 1
            if delayCounter >= RESET_DELAY_FRAMES:
                previousX = None
                delayCounter = 0

    if cv2.waitKey(1) == ord('q'):
        break

    # (optional) display videofeed
    cv2.imshow('Gesture Recognition', frame) 

cap.release()
cv2.destroyAllWindows()