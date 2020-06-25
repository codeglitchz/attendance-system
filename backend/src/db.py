from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    create_engine, MetaData, Table, Column, Integer, String, Date
)

# database for flask server app
db = SQLAlchemy()

# database for cli app
engine = create_engine("sqlite:///test.db", echo=True)
connection = engine.connect()
metadata = MetaData()

moderators = Table(
    'moderators', metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String(80), unique=True, nullable=False),
    Column('password', String(80), nullable=False)
)

students = Table(
    'students', metadata,
    Column('id', Integer(), primary_key=True),
    Column('name', String(255), unique=True, nullable=False)
)

attendance = Table(
    'attendance', metadata,
    Column('date', Date)
)

metadata.create_all(engine)
