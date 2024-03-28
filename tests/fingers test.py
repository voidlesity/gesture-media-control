# Testing fingers

from cvzone.HandTrackingModule import HandDetector
import cv2

detector = HandDetector(detectorCon=0.8, maxHands=2)
video = cv2.VideoCapture(2)

while True:
    ret,frame = video.read()
    hands,img = detector.findHands(frame)
    if hands:
        lmlist = hands[0]
        fingers= detector.fingersUp(lmlist)

        print(fingers)

    cv2.imshow("Frame",frame)
    k=cv2.waitKey(1)
    
    if k==ord('q'):
        
        break

video.release()
cv2.destroyAllWindows()