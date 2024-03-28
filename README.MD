# Gesture Media Control

Control your media with your hands

**this is still under active development following features are being worked on**

- a config page to configure camera, swipe threshold, ...
- systray icon to manage the program
- running in the background
- more gestures/actions
- proper installer

## Installation

1. Download the installer from [here](https://github.com/voidlesity/gesture-media-control/releases/latest)
2. Run through the installation and run the program

## Supported Gestures and Actions

- **Palm Open**: Simulates a play/pause media key press.
- **Swipe Left**: Simulates a press of the previous track media key.
- **Swipe Right**: Simulates a press of the next track media key.

## Exiting the Application

Press `q` while the application window is active to safely close the application.

## Dependencies

Gesture Media Control relies on the following Python libraries:

- `cv2` (OpenCV): For capturing and processing video frames.
- `cvzone`: For hand detection and tracking.
- `pynput`: For simulating keyboard presses to control media playback.

You can install these dependencies by running:

```bash
pip install -r requirements.txt
```

## Contribution

Contributions to Gesture Media Control are welcome! If you have suggestions for improvements or bug fixes, please feel free to open an issue or submit a pull request.
