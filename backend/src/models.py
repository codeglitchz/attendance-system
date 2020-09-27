from typing import List
from uuid import uuid4
from datetime import date as dt, datetime as dtime

from sqlalchemy import Column, Integer, String, Boolean, DateTime, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func


from src.db import Session


Base = declarative_base()


class TeacherModel(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True)
    username = Column(String(80), nullable=False, unique=True)
    password = Column(String(80), nullable=False)

    @classmethod
    def find_by_username(cls, username: str) -> "TeacherModel":
        return Session.query(cls).filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "TeacherModel":
        return Session.query(cls).filter_by(id=_id).first()

    def save_to_db(self) -> None:
        Session.add(self)
        Session.commit()

    def delete_from_db(self) -> None:
        Session.delete(self)
        Session.commit()


class StudentModel(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    attendances = relationship(
        "AttendanceModel",
        backref=backref("student")
    )

    @classmethod
    def find_by_name(cls, name: str) -> "StudentModel":
        return Session.query(cls).filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "StudentModel":
        return Session.query(cls).filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["StudentModel"]:
        return Session.query(cls).all()

    def save_to_db(self) -> None:
        Session.add(self)
        Session.commit()

    def delete_from_db(self) -> None:
        Session.delete(self)
        Session.commit()


class AttendanceModel(Base):
    # One student has many attendances
    # One to Many Relationship
    __tablename__ = "attendances"

    # id = Column(String(50), default=uuid4().hex, primary_key=True)
    # time = Column(TIMESTAMP(timezone=False), default=dtime.now)
    date = Column(DateTime(timezone=True), default=dtime.now, primary_key=True)  # default=func.now
    student_id = Column(Integer, ForeignKey("students.id"))
    # creates AttendanceModel.students as list and
    # backref StudentModel.attendances as AppenderQuery object
    # which can be accessed by StudentModel.attendances.all()
    # students = relationship(
    #     "StudentModel",
    #     # secondary="student_attendances",
    #     foreign_keys="StudentModel.id",
    #     backref=backref("attendances", lazy="dynamic")
    # )

    @classmethod
    def find_by_date(cls, date: dt, student: StudentModel) -> "AttendanceModel":
        return Session.query(cls).filter_by(date=date, student=student).first()

    @classmethod
    def find_by_student(cls, student: StudentModel) -> "AttendanceModel":
        return Session.query(cls).filter_by(student=student).first()

    @classmethod
    def find_by_time(cls, time: dtime) -> "AttendanceModel":
        return Session.query(cls).filter_by(time=time).first()

    @classmethod
    def find_all(cls) -> List["AttendanceModel"]:
        # for x in Session.query(cls, StudentModel).filter(
        #         StudentAttendances.attendance_id == cls.id,
        #         StudentAttendances.student_id == StudentModel.id).order_by(cls.date).all():
        #     print(f"Date: {x.AttendanceModel.date} Name: {x.StudentModel.name} Time: {x.AttendanceModel.time}")
        return Session.query(cls).all()

    @classmethod
    def is_marked(cls, date: dt, student: StudentModel) -> bool:
        marked = AttendanceModel.find_by_date(date, student)
        if marked is None:
            marked = False
        else:
            marked = True
        return marked

    def save_to_db(self) -> None:
        Session.add(self)
        Session.commit()

    def delete_from_db(self) -> None:
        Session.delete(self)
        Session.commit()


class VideoFeedModel(Base):
    __tablename__ = "video_feeds"

    id = Column(String(30), nullable=False, primary_key=True)
    is_active = Column(Boolean, default=False)
    url = Column(String, nullable=False)

    @classmethod
    def find_by_id(cls, _id: str) -> "VideoFeedModel":
        return Session.query(cls).filter_by(id=_id).first()

    @classmethod
    def find_by_url(cls, url: str) -> "VideoFeedModel":
        return Session.query(cls).filter_by(url=url).first()

    @classmethod
    def find_all(cls) -> List["VideoFeedModel"]:
        return Session.query(cls).all()

    def save_to_db(self) -> None:
        Session.add(self)
        Session.commit()

    def delete_from_db(self) -> None:
        Session.delete(self)
        Session.commit()
