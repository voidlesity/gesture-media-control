from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Key, Controller
import cv2

# Constants
SWIPE_THRESHOLD = 200
RESET_DELAY_FRAMES = 15

# Initialize keyboard control and cvzone hand detector
keyboard = Controller()
detector = HandDetector(detectionCon=0.75, maxHands=1)

# Functions
def leftSwipeFunction():
    keyboard.touch(Key.media_previous, True)
    print("Left Swipe Detected!")

def rightSwipeFunction():
    keyboard.touch(Key.media_next, True)
    print("Right Swipe Detected!")

def palmFunction():
    keyboard.touch(Key.media_play_pause, True)
    print("Palm Detected!")

# Main program loop
previousIndexPos = None
previousFingers = None
delayCounter = 0

# Start webcam capture
cap = cv2.VideoCapture(2)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # cvzone processing
    hands, frame = detector.findHands(frame)

    if hands:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        indexPos = hand["lmList"][8][0]

        print(fingers)

        # Palm gesture
        if fingers == [1,1,1,1,1] and (previousFingers == [0,0,0,0,0] or previousFingers == [1,0,0,0,0]) :
            palmFunction()

        # Swipe gestures
        if previousIndexPos is not None:
            if abs(indexPos - previousIndexPos) > SWIPE_THRESHOLD:
                if indexPos > previousIndexPos:
                    leftSwipeFunction()
                else:
                    rightSwipeFunction()

        previousIndexPos = indexPos
        previousFingers = fingers

    else:
        if previousIndexPos is not None:
            delayCounter += 1
            if delayCounter >= RESET_DELAY_FRAMES:
                previousIndexPos = None
                delayCounter = 0
                previousFingers = None


    if cv2.waitKey(1) == ord('q'):
        break

    # (optional) display video feed
    cv2.imshow('Gesture Recognition', frame)

cap.release()
cv2.destroyAllWindows()