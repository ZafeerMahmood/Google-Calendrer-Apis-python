import cv2
import mediapipe as mp
from imutils.video import VideoStream

class PoseDetector:
    def __init__(self, url):
        self.url = url
        self.vs = None
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose

    def start_stream(self):
        self.vs = VideoStream(src=self.url).start()

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

                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

        cv2.destroyAllWindows()
        self.vs.stop()

# Example usage

if __name__ == '__main__':
    url = 'b.mp4'
    pose_detector = PoseDetector(url)
    pose_detector.start_stream()
