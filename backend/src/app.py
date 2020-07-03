from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from marshmallow import ValidationError

from src.resources.dashboard import Dashboard
from src.resources.teacher import Teacher, TeacherRegister, TeacherLogin
from src.resources.student import StudentList, StudentAdd, StudentDelete
from src.resources.attendance import AttendanceList
from src.resources.video_feed import VideoFeed


app = Flask(__name__)
app.config.from_object("src.settings.FlaskAppConfiguration")
api = Api(app)
jwt = JWTManager(app)
cors = CORS(app)


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


api.add_resource(Teacher, "/teacher/<int:teacher_id>")
api.add_resource(TeacherRegister, "/register")
api.add_resource(TeacherLogin, "/login")
api.add_resource(Dashboard, "/dashboard")
api.add_resource(VideoFeed, "/video_feed")
api.add_resource(StudentList, "/students")
api.add_resource(StudentAdd, "/students/add")
api.add_resource(StudentDelete, "/students/delete/<int:student_id>")
api.add_resource(AttendanceList, "/attendance")
