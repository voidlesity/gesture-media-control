# Gesture Media Control

Control your media with your hands

## Installation

1. Download the installer from [here](https://github.com/voidlesity/gesture-media-control/releases/latest)
2. Run through the installation and run the program

## Supported Gestures and Actions

- **Palm Open**: Simulates a play/pause media key press.
- **Swipe Left**: Simulates a press of the previous track media key.
- **Swipe Right**: Simulates a press of the next track media key.

_More Gestures are under development_

## Exiting the Application

Look in your system tray and right click the icon to open the menu where you can quit the program.

## Dependencies

Gesture Media Control relies on the following Python libraries:

- **`configparser`:** Manages user configuration settings for the application.
- **`pyinstaller`:** Packages the Python application into a standalone executable.
- **`mediapipe`:** Provides advanced machine learning models for hand and gesture tracking.
- **`pystray`:** Creates system tray applications, potentially for easy access to controls or settings.
- **`cvzone`:** Simplifies hand detection and tracking for gesture recognition.
- **`pynput`:** Simulates keyboard presses for media control based on gestures.

You can install these dependencies by running:

```bash
pip install -r requirements.txt
```

## Contribution

Contributions to Gesture Media Control are welcome! If you have suggestions for improvements or bug fixes, please feel free to open an issue or submit a pull request.
