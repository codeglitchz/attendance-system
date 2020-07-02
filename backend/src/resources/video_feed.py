import os
import time
from threading import Thread, Lock

import cv2
import numpy
from flask import Response
from flask_restful import Resource

haar_cascade_path = f"files{os.sep}detectors{os.sep}haarcascade_frontalface_alt2.xml"
detector = cv2.CascadeClassifier(haar_cascade_path)


# video_capture = cv2.VideoCapture("files" + os.sep + "video.avi")
# video_capture = cv2.VideoCapture(0)


# def camera_stream():
#     # Capture frame-by-frame
#     ret, frame = video_capture.read()
#
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#
#     faces = detector.detectMultiScale(
#         gray,
#         scaleFactor=1.1,
#         minNeighbors=5,
#         minSize=(30, 30),
#         flags=cv2.CASCADE_SCALE_IMAGE
#     )
#
#     # Draw a rectangle around the faces
#     for (x, y, w, h) in faces:
#         cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
#
#     # Display the resulting frame in browser
#     return cv2.imencode('.jpg', frame)[1].tobytes()
#
#
# def gen_frame():
#     """Video streaming generator function."""
#     while True:
#         frame = camera_stream()
#         print("Generating...")
#         yield (
#                 b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
#         )  # concat frame one by one and show result


class CameraStream:
    thread = None
    frame = None
    last_access = 0

    def __init__(self, stream, src=0):
        self.stream = cv2.VideoCapture(stream)

        (self.grabbed, self.frame) = self.stream.read()
        self.started = False
        self.read_lock = Lock()

    def start(self):
        if self.started:
            print("already started!!")
            return None
        self.started = True
        self.thread = Thread(target=self.update, args=())
        self.thread.start()
        return self

    def update(self):
        while self.started:
            (grabbed, frame) = self.stream.read()
            self.read_lock.acquire()
            self.grabbed, self.frame = grabbed, frame
            self.read_lock.release()

    def read(self):
        self.read_lock.acquire()
        if not isinstance(self.frame, numpy.ndarray):
            # debugging stuff
            print('achtung', type(self.frame))
            return 0

        frame = self.frame.copy()

        self.read_lock.release()
        return frame

    def stop(self):
        self.started = False
        self.thread.join()

    def __exit__(self, exc_type, exc_value, traceback):
        self.stream.release()


class VideoFeed(Resource):
    INPUT_VIDEO = 0

    def get(self):
        response = Response(VideoFeed.gen_frame(self), mimetype='multipart/x-mixed-replace; boundary=frame')
        return response

    def gen_frame(self):
        """
        Video stream generator
        """
        self.cap = CameraStream(self.INPUT_VIDEO).start()
        while self.cap:

            frame = self.cap.read()
            convert = cv2.imencode('.jpg', frame)[1].tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + convert + b'\r\n')  # concate frame one by one and show result

            time.sleep(0.05)

        self.cap.stop()
        cv2.destroyAllWindows()
        self.cap.stream.release()
        print("done")

    def __del__(self):
        try:
            self.cap.stop()
            self.cap.stream.release()
        except:
            print('probably there\'s no cap yet :(')
        cv2.destroyAllWindows()
