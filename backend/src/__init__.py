from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from marshmallow import ValidationError
from dotenv import load_dotenv

from src.db import db
from src.resources.dashboard import Dashboard
from src.resources.user import UserRegister, UserLogin, User
from src.resources.event import Events, SpecialEvents


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
