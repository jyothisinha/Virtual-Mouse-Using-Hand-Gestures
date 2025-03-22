import cv2
import mediapipe as mp
import pyautogui
import random
import util
from pynput.mouse import Button, Controller
import os

mouse = Controller()

screen_width, screen_height = pyautogui.size()

mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=1
)

dragging = False


def find_finger_tip(processed):
    if processed.multi_hand_landmarks:
        hand_landmarks = processed.multi_hand_landmarks[0]  # Assuming only one hand is detected
        index_finger_tip = hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]
        return index_finger_tip
    return None, None


def move_mouse(index_finger_tip):
    if index_finger_tip is not None:
        x = int(index_finger_tip.x * screen_width)
        y = int(index_finger_tip.y / 2 * screen_height)
        pyautogui.moveTo(x, y)


def is_left_click(landmark_list, thumb_index_dist):
    return (
        util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 50 and
        util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) > 90 and
        util.get_angle(landmark_list[13], landmark_list[14], landmark_list[16]) > 90 and
        util.get_angle(landmark_list[20], landmark_list[18], landmark_list[17]) > 90 and
        thumb_index_dist > 50
    )


def is_right_click(landmark_list, thumb_index_dist):
    return (
        util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 50 and
        util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) > 90 and
        util.get_angle(landmark_list[13], landmark_list[14], landmark_list[16]) > 90 and
        util.get_angle(landmark_list[20], landmark_list[18], landmark_list[17]) > 90 and
        thumb_index_dist > 50
    )


def is_double_click(landmark_list, thumb_index_dist):
    return (
        util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 50 and
        util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 50 and
        util.get_angle(landmark_list[13], landmark_list[14], landmark_list[16]) > 90 and
        util.get_angle(landmark_list[20], landmark_list[18], landmark_list[17]) > 90 and
        thumb_index_dist > 50
    )


def is_screenshot(landmark_list, thumb_index_dist):
    return (
       util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 50 and
       util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 50 and
       util.get_angle(landmark_list[13], landmark_list[14], landmark_list[16]) > 90 and
       util.get_angle(landmark_list[20], landmark_list[18], landmark_list[17]) > 90 and
       thumb_index_dist < 50
    )


def is_drag(landmark_list, thumb_index_dist):
    return (
        util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 50 and# Thumb bent
        util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 50 and
        util.get_angle(landmark_list[13], landmark_list[14], landmark_list[16]) < 50 and
        util.get_angle(landmark_list[20], landmark_list[18], landmark_list[17]) < 50 and # Little finger not bent
        thumb_index_dist < 50
    )


def is_drop(landmark_list, thumb_index_dist):
    return (
        util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 50 and# Thumb bent
        util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 50 and
        util.get_angle(landmark_list[13], landmark_list[14], landmark_list[16]) < 50 and
        util.get_angle(landmark_list[20], landmark_list[18], landmark_list[17]) > 90 and # Little finger not bent
        thumb_index_dist < 50
    )


def is_zoom_in(landmark_list, thumb_index_dist):
    return (
        util.get_angle(landmark_list[13], landmark_list[14], landmark_list[16]) < 50 and
        util.get_angle(landmark_list[17], landmark_list[18], landmark_list[20]) < 50 and
        util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) > 90 and# Thumb bent
        util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) > 90 and
        thumb_index_dist > 50
    )


def is_zoom_out(landmark_list):
    return (
        util.get_distance([landmark_list[20], landmark_list[4]]) < 30
    )


def is_scroll_up(landmark_list, thumb_index_dist):
    return (
        util.get_angle(landmark_list[13], landmark_list[14], landmark_list[16]) < 50 and
        util.get_angle(landmark_list[17], landmark_list[18], landmark_list[20]) > 90 and
        thumb_index_dist > 50
    )


def is_scroll_down(landmark_list, thumb_index_dist):
    return (
        util.get_angle(landmark_list[17], landmark_list[18], landmark_list[20]) < 50 and
        util.get_angle(landmark_list[13], landmark_list[14], landmark_list[16]) > 90 and
        thumb_index_dist > 50
    )


def detect_gesture(frame, landmark_list, processed, screenshot_dir):
    global dragging
    if len(landmark_list) >= 21:
        index_finger_tip = find_finger_tip(processed)
        thumb_index_dist = util.get_distance([landmark_list[4], landmark_list[5]])

        if util.get_distance([landmark_list[4], landmark_list[5]]) < 50 and util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) > 90:
            move_mouse(index_finger_tip)
        elif is_left_click(landmark_list, thumb_index_dist):
            mouse.press(Button.left)
            mouse.release(Button.left)
            cv2.putText(frame, "Left Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        elif is_right_click(landmark_list, thumb_index_dist):
            mouse.press(Button.right)
            mouse.release(Button.right)
            cv2.putText(frame, "Right Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        elif is_double_click(landmark_list, thumb_index_dist):
            pyautogui.doubleClick()
            cv2.putText(frame, "Double Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        elif is_screenshot(landmark_list, thumb_index_dist):
            im1 = pyautogui.screenshot()
            label = random.randint(1, 1000)
            screenshot_path = os.path.join(screenshot_dir, f'my_screenshot_{label}.png')
            im1.save(screenshot_path)
            cv2.putText(frame, "Screenshot Taken", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        elif is_zoom_in(landmark_list, thumb_index_dist):
            pyautogui.hotkey('ctrl', '+')
            cv2.putText(frame, "Zoom In", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        elif is_zoom_out(landmark_list):
            pyautogui.hotkey('ctrl', '-')
            cv2.putText(frame, "Zoom Out", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
        elif is_scroll_up(landmark_list, thumb_index_dist):
            mouse.scroll(0, 2)
            cv2.putText(frame, "Scroll Up", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        elif is_scroll_down(landmark_list, thumb_index_dist):
            mouse.scroll(0, -2)
            cv2.putText(frame, "Scroll Down", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        elif is_drag(landmark_list, thumb_index_dist):
            if not dragging:
                mouse.press(Button.left)
                dragging = True
            move_mouse(index_finger_tip)
            cv2.putText(frame, "Dragging", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        elif is_drop(landmark_list, thumb_index_dist):
            if dragging:
                mouse.release(Button.left)
                dragging = False
            cv2.putText(frame, "Dropped", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)


def main(screenshot_dir):
    draw = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(0)

    try:
        cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)
        cv2.setWindowProperty('Frame', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Frame', screen_width, screen_height)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            processed = hands.process(frameRGB)

            landmark_list = []
            if processed.multi_hand_landmarks:
                hand_landmarks = processed.multi_hand_landmarks[0]  # Assuming only one hand is detected
                draw.draw_landmarks(frame, hand_landmarks, mpHands.HAND_CONNECTIONS)
                for lm in hand_landmarks.landmark:
                    landmark_list.append((lm.x, lm.y))

            detect_gesture(frame, landmark_list, processed, screenshot_dir)

            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    screenshot_directory = r'D:\Virtual mouse\Screen Shorts'  # Change this to your desired directory
    main(screenshot_directory)