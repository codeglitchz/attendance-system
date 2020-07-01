import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///files/data.db")

echo = True if eval(os.environ.get("DEVELOPMENT")) else False
engine = create_engine(DATABASE_URL, echo=echo)

# The key here is scoped_session: Now when we use Session, SQLAlchemy will check to see
# if a thread-local session exists. If it already exists, then it will use it,
# otherwise it will create one first.
Session = scoped_session(sessionmaker(bind=engine))
