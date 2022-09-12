"""Handles the motion capture using Mediapipe Pose."""

import threading
import cv2
import mediapipe as mp

class MotionCapture(threading.Thread):
    """Tracks the skeleton keypoints either from a camera stream or a video.
    """

    def __init__(self):
        super().__init__(None)
        self.pose = mp.solutions.pose.Pose(min_detection_confidence = 0.5,
            min_tracking_confidence = 0.5)
        self.drawing = mp.solutions.drawing_utils
        self.is_running = False

    def run(self):
        print("Run called")
        self.camera_capture()

    def camera_capture(self):
        """Uses the video stream of the camera as input to the Mediapipe Pose.
        """
        cap = cv2.VideoCapture(0)

        while self.is_running:
            ret, frame = cap.read()
            if frame is not None:
                frame.flags.writeable = False
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.pose.process(frame)

                frame.flags.writeable = True
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

                self.drawing.draw_landmarks(frame, results.pose_landmarks,
                    mp.solutions.pose.POSE_CONNECTIONS)

                cv2.imshow("Frame", frame)
                cv2.waitKey(1)

        cap.release()
        cv2.destroyAllWindows()

    def start_camera_capture(self):
        "Sets is_running to True."
        self.is_running = True

    def stop_camera_capture(self):
        "Sets is_running to False."
        self.is_running = False

    def video_capture(self, file_path):
        """Captures the keypoints of a pose from a video."""
