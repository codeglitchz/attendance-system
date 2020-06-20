from src import app
from src.db import db
from src.ma import ma


@app.before_first_request
def create_tables():
    db.create_all()


db.init_app(app)
ma.init_app(app)

if __name__ == "__main__":
    app.run(port=5000)
