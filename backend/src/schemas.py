from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow_sqlalchemy.fields import Nested

from src.models import TeacherModel, StudentModel, AttendanceModel


class TeacherSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TeacherModel
        load_only = ("password",)  # during deserialization dictionary -> object
        dump_only = ("id",)  # during serialization object -> dictionary
        load_instance = True  # Optional: deserialize to object/model instances


class StudentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = StudentModel
        # load_only = ()  # during deserialization dictionary -> object
        dump_only = ("id",)  # during serialization object -> dictionary
        load_instance = True  # Optional: deserialize to object/model instances


class AttendanceSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = AttendanceModel
        # load_only = ()  # during deserialization dictionary -> object
        dump_only = ("date", "time", "students")  # during serialization object -> dictionary
        load_instance = True  # Optional: deserialize to object/model instances
    # Override books field to use a nested representation rather than pks
    students = Nested(
        StudentSchema,
        many=True
    )
