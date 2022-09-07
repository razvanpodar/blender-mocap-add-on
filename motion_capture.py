import cv2
import mediapipe as mp

class MotionCapture():

    def __init__(self):
        self.pose = mp.solutions.pose.Pose(min_detection_confidence=0.5,
            min_tracking_confidence=0.5)

    def capture(self):
        pass
