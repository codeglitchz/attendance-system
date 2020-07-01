from typing import List

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
# from sqlalchemy.orm import relationship, backref

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


# class AttendanceModel(Base):
#     # Many students have many attendances
#     # Many to Many Relationship
#     __tablename__ = "attendance"
