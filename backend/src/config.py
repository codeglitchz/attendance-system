import os

DEBUG = True if eval(os.environ.get('DEVELOPMENT')) else False
PROPAGATE_EXCEPTIONS = True
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///files/data.db")
SECRET_KEY = os.environ["SECRET_KEY"]
JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
