# Virtual-Mouse-Using-Hand-Gestures
This repository contains a gesture-based virtual mouse that allows users to control their computer's mouse using hand gestures detected via a webcam. The system is built using OpenCV, MediaPipe, PyAutoGUI, and Pynput to recognize hand landmarks and perform various mouse operations without needing physical contact.

Features:

1. Cursor Control: Move the mouse pointer by moving your index finger.

2. Left Click: Perform a left click using a designated hand gesture.

3. Right-click: Trigger a right-click with another gesture.

4. Double Click: Execute a double-click action seamlessly.

5. Drag & Drop: Hold and release objects with smooth gesture-based drag functionality.

6. Scroll Up/Down: Navigate through pages using intuitive hand movements.

7. Zoom In/Out: Adjust zoom levels with pinch gestures.

8. Screenshot Capture: Capture the screen using a predefined hand sign.

Technologies Used:

1. Python

2. OpenCV – Image processing and computer vision

3. MediaPipe – Hand tracking and gesture recognition

4. PyAutoGUI – Simulating mouse actions

5. Pynput – Controlling input devices

How It Works:

1. The webcam captures real-time video input.

2. MediaPipe processes hand landmarks and detects finger positions.

3. The system analyzes gestures and maps them to corresponding mouse actions.

4. PyAutoGUI and Pynput execute the detected operations.
