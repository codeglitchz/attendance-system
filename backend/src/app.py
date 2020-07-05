from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from marshmallow import ValidationError

from src.resources.dashboard import Dashboard
from src.resources.teacher import Teacher, TeacherRegister, TeacherLogin
from src.resources.student import StudentList, StudentAdd, StudentDelete
from src.resources.attendance import AttendanceList
from src.resources.video_feed import (
    VideoFeedList, VideoFeedAdd, VideoFeed, VideoFeedPreview, VideoFeedStop, VideoFeedStart, VideoFeedDelete
)


app = Flask(__name__)
app.config.from_object("src.settings.FlaskAppConfiguration")
api = Api(app)
jwt = JWTManager(app)
cors = CORS(app)


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


# /teacher
api.add_resource(Teacher, "/teacher/<int:teacher_id>")
api.add_resource(TeacherRegister, "/register")
api.add_resource(TeacherLogin, "/login")

# /dashboard
api.add_resource(Dashboard, "/dashboard")

# /video_feed
api.add_resource(VideoFeedList, "/video_feeds")
api.add_resource(VideoFeedAdd, "/video_feeds/add")
api.add_resource(VideoFeed, "/video_feeds/<string:feed_id>")
api.add_resource(VideoFeedPreview, "/video_feeds/preview/<string:feed_id>")
api.add_resource(VideoFeedStop, "/video_feeds/stop/<string:feed_id>")
api.add_resource(VideoFeedStart, "/video_feeds/start/<string:feed_id>")
api.add_resource(VideoFeedDelete, "/video_feeds/delete/<string:feed_id>")

# /students
api.add_resource(StudentList, "/students")
api.add_resource(StudentAdd, "/students/add")
api.add_resource(StudentDelete, "/students/delete/<int:student_id>")

# /attendance
api.add_resource(AttendanceList, "/attendance")
