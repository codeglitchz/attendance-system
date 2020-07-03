from src.app import app
from src.db import engine, Session
from src.models import Base


# create all the required tables from `src/models.py` before app's first request
@app.before_first_request
def create_tables():
    Base.metadata.create_all(engine)


# The @app.teardown_appcontext decorator will cause the supplied callback, cleanup, to be executed
# when the current application context is torn down. This happens after each request.
# That way we make sure to release the resources used by a session after each request.
@app.teardown_appcontext
def cleanup(resp_or_exc):
    Session.remove()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True)
