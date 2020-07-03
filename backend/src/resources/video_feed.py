from flask import Response
from flask_restful import Resource

from src.libs.camera_opencv import RecognitionCamera


class VideoFeed(Resource):
    @classmethod
    def get(cls):
        """Video streaming route "/video_feed". Put this in the src attribute of an img tag."""
        return Response(
            VideoFeed.gen_frame(RecognitionCamera()),
            mimetype='multipart/x-mixed-replace; boundary=frame'
        )

    @classmethod
    def gen_frame(cls, camera):
        """Video streaming generator function."""
        while True:
            frame = camera.get_frame()
            yield (
                    b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
            )  # concat frame one by one and show result
