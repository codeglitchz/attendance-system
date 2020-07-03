import cv2

from src.libs.base_camera import BaseCamera
from src.settings import VIDEO_SOURCE


class RecognitionCamera(BaseCamera):
    video_source = 0

    def __init__(self):
        if VIDEO_SOURCE:
            RecognitionCamera.set_video_source(VIDEO_SOURCE)
        super(RecognitionCamera, self).__init__()

    @classmethod
    def set_video_source(cls, source):
        cls.video_source = source

    @classmethod
    def frames(cls):
        camera = cv2.VideoCapture(cls.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        while True:
            # read current frame
            _, img = camera.read()

            # TODO: logic of recognition or detection

            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()
