from tkinter import Tk, Label, Entry, Button, StringVar, Frame, Toplevel, messagebox
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Key, Controller
from PIL import Image
import configparser
import pystray
import cv2
import sys
import os

# Read and Update Config Functions
def readConfig():
    config = configparser.ConfigParser()
    if os.path.exists(configFilePath):
        config.read(configFilePath)
    else:
        config['DEFAULT'] = {
            'camera_index': '0',
            'show_preview': 'False',
            'swipe_threshold': '200',
            'reset_delay_frames': '15',
            'detection_confidence': '0.8',
        }
        with open(configFilePath, 'w') as configfile:
            config.write(configfile)
    return config

def updateConfig():

    def onSubmit():
        for var in allVars:
            config['DEFAULT'][var] = entries[var].get().replace(" ", "")
        with open(configFilePath, 'w') as configfile:
            config.write(configfile)
        root.destroy()

        os.execl(sys.executable, sys.executable, *sys.argv)

    def checkEntries(*args):
        if all(entries[var].get() for var in allVars):
            submitButton.config(state='normal')
        else:
            submitButton.config(state='disabled')

    root = Tk()
    root.iconbitmap("icon.ico")
    root.title("Gesture Media Control")
    root.geometry("300x450")
    root.protocol("WM_DELETE_WINDOW", root.destroy)
    root.configure(bg='#2E2E2E')
    
    entries = {}
    for var in allVars:
        label = Label(root, text=var.replace('_', ' ').title(), bg='#2E2E2E', fg='#FFFFFF', font=("Tahoma Regular", 16))
        label.pack(pady=5)

        entryText = StringVar()
        entryText.set(config['DEFAULT'].get(var, ''))
        entryText.trace("w", checkEntries)

        entry = Entry(root, textvariable=entryText, width=20, bg='#555555', fg='#FFFFFF', insertbackground='grey', font=("Tahoma Regular", 16))
        entry.pack(pady=5)

        entries[var] = entryText

    buttonFrame = Frame(root, bg='#2E2E2E')
    buttonFrame.pack(side="bottom", fill="both", pady=10)

    submitButton = Button(buttonFrame, text="Submit", command=onSubmit, bg='#333333', fg='#FFFFFF', font=("Tahoma Regular", 16), state='disabled')
    submitButton.pack(side="right", padx=5)

    cancelButton = Button(buttonFrame, text="Cancel", command=root.destroy, bg='#333333', fg='#FFFFFF', font=("Tahoma Regular", 16))
    cancelButton.pack(side="right")

    checkEntries()

    root.mainloop()


# Gestures
def leftSwipeFunction():
    keyboard.touch(Key.media_previous, True)
    print("Left Swipe Detected!")

def rightSwipeFunction():
    keyboard.touch(Key.media_next, True)
    print("Right Swipe Detected!")

def palmFunction():
    keyboard.touch(Key.media_play_pause, True)
    print("Palm Detected!")


# System tray icon functions
def configureFunction():
    updateConfig()

def togglePreviewFunction(icon, item):
    global SHOW_PREVIEW
    SHOW_PREVIEW = not SHOW_PREVIEW

def quitFunction(icon, item):
    icon.stop()
    cap.release()
    cv2.destroyAllWindows()

# Main program loop
if __name__ == '__main__':

    allVars = ['camera_index', 'detection_confidence',  'show_preview', 'swipe_threshold', 'reset_delay_frames']

    # Configuration
    configFilePath = os.path.join(os.path.expanduser("~"), ".config", "voidlesity", "GestureMediaControl.ini")
    os.makedirs(os.path.dirname(configFilePath), exist_ok=True)
    config = readConfig()

    if [var for var in allVars if not config['DEFAULT'].get(var)]:
        updateConfig()

    CAMERA_INDEX = int(config['DEFAULT'].get('camera_index'))
    SHOW_PREVIEW = config['DEFAULT'].getboolean('show_preview')
    SWIPE_THRESHOLD = float(config['DEFAULT'].get('swipe_threshold'))
    RESET_DELAY_FRAMES = float(config['DEFAULT'].get('reset_delay_frames'))
    DETECTION_CONFIDENCE = float(config['DEFAULT'].get('detection_confidence'))

    # Initialize keyboard control and cvzone hand detector
    keyboard = Controller()
    detector = HandDetector(detectionCon=DETECTION_CONFIDENCE, maxHands=1)

    # System tray icon
    image = Image.open("icon.ico")
    menu = (
        pystray.MenuItem("Toggle Preview", togglePreviewFunction),
        pystray.MenuItem("Configure", configureFunction),
        pystray.MenuItem("Quit", quitFunction)
    )
    pystray.Icon("Gesture Media Control", image, "Gesture Media Control", menu).run_detached()


    previousIndexPos = None
    previousFingers = None
    delayCounter = 0

    # Start webcam capture
    cap = cv2.VideoCapture(CAMERA_INDEX)
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

        if SHOW_PREVIEW:
            cv2.imshow('Gesture Media Control', frame)
        else:
            cv2.destroyAllWindows()

        cv2.waitKey(1)

    cap.release()
    cv2.destroyAllWindows()