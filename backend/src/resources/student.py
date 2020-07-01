from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from src.db import Session
from src.libs.strings import gettext
from src.models import StudentModel
from src.schemas import StudentSchema

student_schema = StudentSchema()
student_list_schema = StudentSchema(many=True)


class StudentList(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        return student_list_schema.dump(StudentModel.find_all()), 200


class StudentAdd(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        student_json = request.get_json()

        student = student_schema.load(student_json, session=Session)

        try:
            student.save_to_db()
        except:
            return {"message": gettext('error_inserting')}, 500

        return student_schema.dump(student), 201


class StudentDelete(Resource):
    @classmethod
    @jwt_required
    def delete(cls, student_id: int):
        student = StudentModel.find_by_id(student_id)
        if student:
            student.delete_from_db()
            return {"message": gettext('student_deleted').format(student.name, student.id)}, 200

        return {"message": gettext('student_not_found')}, 404
