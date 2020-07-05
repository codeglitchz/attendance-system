from flask import Response, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.db import Session
from src.libs.strings import gettext
from src.models import VideoFeedModel
from src.schemas import VideoFeedSchema
from src.libs.web_utils import RecognitionCamera


video_feed_schema = VideoFeedSchema()
video_feed_list_schema = VideoFeedSchema(many=True)


# TODO: change this to support multiple feeds
class VideoFeedList(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        return video_feed_list_schema.dump(VideoFeedModel.find_all()), 200


class VideoFeed(Resource):
    @classmethod
    @jwt_required
    def get(cls, feed_id: str):
        """Video streaming route "/video_feed". Put this in the src attribute of an img tag."""
        video_feed = VideoFeedModel.find_by_id(feed_id)

        if video_feed:
            return video_feed_schema.dump(video_feed), 200

        return {"message": gettext('video_feed_not_found')}, 404


# TODO: make this get() to work with @jwt_required by sending response with Flask-RESTful instead of Response()
class VideoFeedPreview(Resource):
    @classmethod
    def get(cls, feed_id: str):
        """Video streaming route. Put this route in the src attribute of an img tag."""
        video_feed = VideoFeedModel.find_by_id(feed_id)
        feed_url = video_feed.url
        camera_stream = RecognitionCamera
        if feed_url == "0":
            feed_url = 0
        camera_stream.set_video_source(feed_url)
        if video_feed:
            resp = Response(
                cls.gen_frame(camera_stream(unique_id=feed_id)),
                mimetype='multipart/x-mixed-replace; boundary=frame'
            )
            return resp

        return {"message": gettext('video_feed_not_found')}, 404

    @classmethod
    def gen_frame(cls, camera):
        """Video streaming generator function."""
        while True:
            frame = camera.get_frame()
            yield (
                    b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
            )  # concat frame one by one and show result


# TODO: VideoFeedAdd Resource
class VideoFeedAdd(Resource):
    """Adds a video feed to `feeds` table in the database"""
    @classmethod
    @jwt_required
    def post(cls):
        video_feed_json = request.get_json()

        video_feed = video_feed_schema.load(video_feed_json, session=Session)

        try:
            video_feed.save_to_db()
        except:
            return {"message": gettext('error_inserting')}, 500

        return video_feed_schema.dump(video_feed), 201


class VideoFeedStop(Resource):
    @classmethod
    @jwt_required
    def get(cls, feed_id: str):
        video_feed = VideoFeedModel.find_by_id(feed_id)
        if video_feed:
            RecognitionCamera.stop(feed_id)
            try:
                video_feed.is_active = False
                video_feed.save_to_db()
            except:
                return {"message": gettext('internal_server_error')}, 500
            return {"message": gettext('video_feed_stopped')}, 200

        return {"message": gettext('video_feed_not_found')}, 404


class VideoFeedStart(Resource):
    """Restart video feed for specific feed given by its feed_id"""
    @classmethod
    @jwt_required
    def get(cls, feed_id: str):
        video_feed = VideoFeedModel.find_by_id(feed_id)
        if video_feed:
            # RecognitionCamera.start_feed()
            try:
                video_feed.is_active = True
                video_feed.save_to_db()
            except:
                return {"message": gettext('internal_server_error')}, 500
            return {"message": gettext('video_feed_stopped')}, 200

        return {"message": gettext('video_feed_not_found')}, 404


class VideoFeedDelete(Resource):
    @classmethod
    @jwt_required
    def delete(cls, feed_id: str):
        video_feed = VideoFeedModel.find_by_id(feed_id)
        if video_feed:
            video_feed.delete_from_db()
            return {"message": gettext('video_feed_deleted').format(video_feed.id)}, 200

        return {"message": gettext('video_feed_not_found')}, 404
