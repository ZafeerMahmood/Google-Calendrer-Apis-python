"""pose estimation module
This module is used to detect a pose and create a Google Calendar event if the user is detected to be sitting for
more than 10 seconds(changeable)."""
import cv2
import mediapipe as mp
from google_calendar import create_event, get_credentials
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta

class PoseDetector:
    def __init__(self, url):
        self.url = url
        self.secs = 10  # change this to change the time threshold eg 300 for 5 minutes
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.last_detection_time = None
        self.black_screen_start_time = None

    def detect_pose(self, video_path):
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            print("Error opening video")
            return

        with self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

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
                if results.pose_landmarks and any(landmark.visibility > 0.5 for landmark in results.pose_landmarks.landmark):
                    self.pose_detected_actions()
                else:
                    self.pose_not_detected_actions()

                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

        cap.release()
        cv2.destroyAllWindows()

    def pose_detected_actions(self):
        if self.last_detection_time is None:
            self.last_detection_time = datetime.now()
            self.black_screen_start_time = None  # Reset black screen timer

    def pose_not_detected_actions(self):
        if self.last_detection_time is not None:
            time_difference = datetime.now() - self.last_detection_time
            if time_difference.total_seconds() >= self.secs:  # Adjust the time threshold as needed
                self.handle_black_screen()

    def handle_black_screen(self):
        if self.black_screen_start_time is None:
            self.black_screen_start_time = datetime.now()
        else:
            black_screen_duration = datetime.now() - self.black_screen_start_time
            if black_screen_duration.total_seconds() >= self.secs:
                try:
                    start_time = self.last_detection_time.isoformat()
                    end_time = (self.last_detection_time + timedelta(seconds=10)).isoformat()
                    event_link = create_event("Work Time", "Home", "Work session", start_time, end_time,
                                              [], [], {'useDefault': False, 'overrides': [{'method': 'popup', 'minutes': 10}]})
                    print('Event created:', event_link)
                except HttpError as error:
                    print('An error occurred:', error)
                self.last_detection_time = None
                self.black_screen_start_time = None

# Example usage
if __name__ == '__main__':
    get_credentials()
    get_credentials()
    video_path = 'b.mp4'  # Replace with the actual path to your video file
    pose_detector = PoseDetector(video_path)
    pose_detector.detect_pose(video_path)

