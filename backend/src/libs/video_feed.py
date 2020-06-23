import os
import cv2

haar_cascade_path = "files" + os.sep + "haarcascade_frontalface_default.xml"
detector = cv2.CascadeClassifier(haar_cascade_path)

# video_capture = cv2.VideoCapture("files" + os.sep + "video.avi")
video_capture = cv2.VideoCapture(0)


def camera_stream():
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the resulting frame in browser
    return cv2.imencode('.jpg', frame)[1].tobytes()


def gen_frame():
    """Video streaming generator function."""
    while True:
        frame = camera_stream()
        yield (
                b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
        )  # concat frame one by one and show result
