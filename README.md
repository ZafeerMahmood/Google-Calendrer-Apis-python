# Google Calendar APIs Python Integration
This repository contains simple Python scripts to interact with the Google Calendar APIs. The google_calendar.py module provides functions for utilizing the Google Calendar API, while the google.py script serves as a testing example.

# Setup and Run
To run the scripts, follow these steps:

Install the required dependencies by executing the following command in your terminal or command prompt:

bash
Copy code
```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client google-auth-oauthlib
```
Run the google.py script
Copy code
```bash
py google.py
```
Please note that you need to enable the Google Calendar API for this integration to work. Follow Google's documentation to enable the API and obtain your API credentials.

# Pose Estimation

This project now includes a `PoseDetector` class that performs real-time pose estimation using the Mediapipe library. The `PoseDetector` class accepts a video stream URL and provides visual feedback of detected poses.

# Usage

To use the `PoseDetector` class:

1. Import the class into your script:

    ```python
    from pose_detector import PoseDetector
    ```

2. Create an instance of the `PoseDetector` class with the video stream URL:

    ```python
    url = 'b.mp4'  # Replace with your video stream URL
    pose_detector = PoseDetector(url)
    ```

3. Start the pose estimation and visualization:

    ```python
    pose_detector.start_stream()
    ```
this automaticly creats a google calender event as soon a person stop working 
and add the time the person worked for

# Future Plans
This project is designed to be easily extendable. The modular structure allows for future expansion and integration, such as creating a Flask web service to provide Google Calendar functionality over the web.

# Contributions
Contributions are welcome! If you have ideas to improve or expand this project, feel free to open an issue or submit a pull request.

# Disclaimer
This project is for educational and illustrative purposes only. Make sure to adhere to Google's API usage policies and best practices.


