from src.ma import ma
from src.models.student import StudentModel


class StudentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = StudentModel
        # load_only = ()
        dump_only = ("id",)
        load_instance = True
