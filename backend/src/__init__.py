from flask import Flask, jsonify, Response
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from marshmallow import ValidationError
from dotenv import load_dotenv

from src.db import db
from src.resources.dashboard import Dashboard
from src.resources.user import UserRegister, UserLogin, User
from src.resources.event import Events, SpecialEvents
from src.resources.student import StudentList, StudentAdd, StudentDelete
from src.resources.attendance import Attendance
from src.libs.video_feed import gen_frame


app = Flask(__name__)
load_dotenv(".env")  # imports from top level directory
app.config.from_object("src.default_config")  # imports from src
app.config.from_envvar("APPLICATION_SETTINGS")  # imports from src
api = Api(app)
jwt = JWTManager(app)
cors = CORS(app)


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(Events, "/events")
api.add_resource(SpecialEvents, "/special")
api.add_resource(Dashboard, "/dashboard")
api.add_resource(StudentList, "/students")
api.add_resource(StudentAdd, "/students/add")
api.add_resource(StudentDelete, "/students/delete/<int:student_id>")
api.add_resource(Attendance, "/attendance")


@app.route('/video_feed')
# TODO: @jwt_required not working
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')
