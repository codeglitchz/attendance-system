from flask_restful import Resource
from flask import request
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token
)

from src.db import Session
from src.libs.strings import gettext
from src.models import TeacherModel
from src.schemas import TeacherSchema

teacher_schema = TeacherSchema()


class Teacher(Resource):
    """
    This resource can be useful when testing our Flask app. We may not want to expose it to public users, but for the
    sake of demonstration in this course, it can be useful when we are manipulating data regarding the users.
    """

    @classmethod
    def get(cls, teacher_id: int):
        teacher = TeacherModel.find_by_id(teacher_id)
        if not teacher:
            return {"message": gettext("teacher_not_found")}, 404

        return teacher_schema.dump(teacher), 200

    @classmethod
    def delete(cls, teacher_id: int):
        teacher = TeacherModel.find_by_id(teacher_id)
        if not teacher:
            return {"message": gettext("teacher_not_found")}, 404

        teacher.delete_from_db()
        return {"message": gettext("teacher_deleted")}, 200


class TeacherRegister(Resource):
    @classmethod
    def post(cls):
        teacher_json = request.get_json()
        teacher = teacher_schema.load(teacher_json, session=Session)

        if TeacherModel.find_by_username(teacher.username):
            return {"message": gettext("teacher_username_exists")}, 400

        teacher.save_to_db()

        return {"message": gettext("teacher_registered")}, 201


class TeacherLogin(Resource):
    @classmethod
    def post(cls):
        teacher_json = request.get_json()
        teacher_data = teacher_schema.load(teacher_json, session=Session)

        teacher = TeacherModel.find_by_username(teacher_data.username)

        if teacher and safe_str_cmp(teacher.password, teacher_data.password):
            access_token = create_access_token(identity=teacher.id, fresh=True)
            refresh_token = create_refresh_token(teacher.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        return {"message": gettext("teacher_invalid_credentials")}, 401
