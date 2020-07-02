from typing import List
from datetime import date as dt, datetime as dtime

from sqlalchemy import Column, Integer, String, Date, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref


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


class StudentAttendances(Base):
    __tablename__ = "student_attendances"
    student_id = Column(Integer, ForeignKey("students.id"), primary_key=True)
    date = Column(Date, ForeignKey("attendances.date"), primary_key=True)


class StudentModel(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    # attendances = relationship(
    #     "AttendanceModel",
    #     secondary="student_attendances",
    #     # backref=backref("students", lazy="dynamic")
    # )

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
    # Many students have many attendances
    # Many to Many Relationship
    __tablename__ = "attendances"

    # id = Column(String(50), default=uuid4().hex, primary_key=True)
    date = Column(Date, default=dt.today, primary_key=True)
    # TODO: change time to show each student's time rather than 1 static time
    time = Column(TIMESTAMP(timezone=False), default=dtime.now)
    # creates AttendanceModel.students as list and
    # backref StudentModel.attendances as AppenderQuery object
    # which can be accessed by StudentModel.attendances.all()
    students = relationship(
        "StudentModel",
        secondary="student_attendances",
        backref=backref("attendances", lazy="dynamic")
    )

    @classmethod
    def find_by_date(cls, date: dt) -> "AttendanceModel":
        return Session.query(cls).filter_by(date=date).first()

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

    def is_student_present(self, student: StudentModel) -> bool:
        return student in self.students

    def save_to_db(self) -> None:
        Session.add(self)
        Session.commit()

    def delete_from_db(self) -> None:
        Session.delete(self)
        Session.commit()
