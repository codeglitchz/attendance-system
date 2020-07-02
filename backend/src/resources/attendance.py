from flask_restful import Resource
from flask_jwt_extended import jwt_required

from src.models import AttendanceModel
from src.schemas import AttendanceSchema

attendance_list_schema = AttendanceSchema(many=True)


class AttendanceList(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        return attendance_list_schema.dump(AttendanceModel.find_all()), 200
