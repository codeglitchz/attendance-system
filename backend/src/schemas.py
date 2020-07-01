from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from src.models import TeacherModel
from src.models import StudentModel


class TeacherSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TeacherModel
        load_only = ("password",)
        dump_only = ("id",)
        load_instance = True  # Optional: deserialize to model instances


class StudentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = StudentModel
        # load_only = ()
        dump_only = ("id",)
        load_instance = True  # Optional: deserialize to model instances
