from src.db import db


class AttendanceModel(db.Model):
    # Many students have many attendances
    # Many to Many Relationship
    __tablename__ = "attendance"
