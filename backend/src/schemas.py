from typing import Union, Any, Optional, Mapping
from werkzeug.datastructures import FileStorage

from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested

from src.models import TeacherModel, StudentModel, AttendanceModel, VideoFeedModel


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
        dump_only = ("date", "student")  # during serialization object -> dictionary
        load_instance = True  # Optional: deserialize to object/model instances
    student = Nested(
        StudentSchema
    )


class VideoFeedSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = VideoFeedModel
        # load_only = ()  # during deserialization dictionary -> object
        dump_only = ("is_active",)  # during serialization object -> dictionary
        load_instance = True  # Optional: deserialize to object/model instances


class FileStorageField(fields.Field):
    default_error_messages = {
        "invalid": "Not a valid image."
    }

    def _deserialize(self, value: Any, attr: Optional[str], data: Optional[Mapping[str, Any]], **kwargs) -> \
            Union[FileStorage, None]:
        if value is None:
            return None
        if not isinstance(value, FileStorage):
            self.fail("invalid")  # raises ValidationError
        return value


class ImageSchema(Schema):
    image = FileStorageField(required=True)
