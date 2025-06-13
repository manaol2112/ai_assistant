"""
gesture_control.py
Premium Hand Gesture Recognition for Robot Control (OpenCV)
"""
import sys
import platform

try:
    import cv2
    import numpy as np
except ImportError:
    cv2 = None
    np = None

class HandGestureController:
    """
    HandGestureController uses OpenCV to detect hand gestures for robot control.
    Returns: 'forward', 'backward', 'left', 'right', 'stop', or None.
    """
    def __init__(self, camera_index=0):
        if cv2 is None or np is None:
            print("[HandGestureController] OpenCV not available. Gesture control disabled.")
            self.enabled = False
            return
        self.cap = cv2.VideoCapture(camera_index)
        self.enabled = self.cap.isOpened()
        if not self.enabled:
            print("[HandGestureController] Camera not available. Gesture control disabled.")

    def get_gesture(self):
        if not self.enabled:
            return None
        ret, frame = self.cap.read()
        if not ret:
            return None
        # Simple demo: count fingers using contour/convexity defects
        roi = frame[100:400, 100:400]
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        upper_skin = np.array([20, 255, 255], dtype=np.uint8)
        mask = cv2.inRange(hsv, lower_skin, upper_skin)
        kernel = np.ones((3,3), np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=4)
        mask = cv2.GaussianBlur(mask, (5,5), 100)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) == 0:
            return None
        cnt = max(contours, key=lambda x: cv2.contourArea(x))
        epsilon = 0.0005*cv2.arcLength(cnt,True)
        approx= cv2.approxPolyDP(cnt,epsilon,True)
        hull = cv2.convexHull(cnt)
        areahull = cv2.contourArea(hull)
        areacnt = cv2.contourArea(cnt)
        arearatio = ((areahull-areacnt)/areacnt)*100 if areacnt != 0 else 0
        hull = cv2.convexHull(approx, returnPoints=False)
        defects = cv2.convexityDefects(approx, hull) if hull is not None and len(hull) > 3 else None
        l=0
        if defects is not None:
            for i in range(defects.shape[0]):
                s,e,f,d = defects[i,0]
                start = tuple(approx[s][0])
                end = tuple(approx[e][0])
                far = tuple(approx[f][0])
                a = np.linalg.norm(np.array(end)-np.array(start))
                b = np.linalg.norm(np.array(far)-np.array(start))
                c = np.linalg.norm(np.array(end)-np.array(far))
                angle = np.arccos((b**2 + c**2 - a**2)/(2*b*c+1e-5))
                if angle <= np.pi/2:
                    l += 1
        fingers = l+1
        # Map number of fingers to actions
        if fingers == 1:
            return 'forward'
        elif fingers == 2:
            return 'backward'
        elif fingers == 3:
            return 'left'
        elif fingers == 4:
            return 'right'
        elif fingers == 5:
            return 'stop'
        else:
            return None
    def release(self):
        if self.enabled:
            self.cap.release() 