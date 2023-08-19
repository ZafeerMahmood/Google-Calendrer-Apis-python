"""pose estimation module
This module is used to detect a pose and create a Google Calendar event if the user is detected to be sitting for
more than 10 seconds(changeable)."""
import cv2
import mediapipe as mp
from imutils.video import VideoStream
from google_calendar import create_event,get_credentials
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta


class PoseDetector:

    def __init__(self, url):
        self.url = url
        self.vs = None
        self.secs=10 # change this to change the time threshold eg 300 for 5 minutes
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose

    def detect_pose(self):
        last_detection_time = None
        pose_detected = False
        
        with self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while True:
                frame = self.vs.read()
                if frame is None:
                    continue

                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False

                results = pose.process(image)

                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                self.mp_drawing.draw_landmarks(
                    image, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS,
                    self.mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                    self.mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                )

                cv2.imshow('Mediapipe Feed', image)

                # Check if a pose is detected
                if any(landmark.visibility > 0.5 for landmark in results.pose_landmarks.landmark):
                    pose_detected = True
                    if last_detection_time is None:
                        last_detection_time = datetime.now()
                else:
                    pose_detected = False
                    if last_detection_time is not None:
                        time_difference = datetime.now() - last_detection_time
                        if time_difference.total_seconds() >= self.secs:  # Adjust the time threshold as needed
                            try:
                                create_event("Work Time", "Home", "Work session", last_detection_time.isoformat(),
                                             (last_detection_time + timedelta(seconds=10)).isoformat(),
                                             [], [], {'useDefault': False, 'overrides': [{'method': 'popup', 'minutes': 10}]})
                            except HttpError as error:
                                print('An error occurred:', error)
                            last_detection_time = None

                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

        cv2.destroyAllWindows()
        self.vs.stop()

# Example usage
if __name__ == '__main__':
    url = 'b.mp4'
    get_credentials()
    pose_detector = PoseDetector(url)
    pose_detector.detect_pose()
