from flask import Flask
from database import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://vaalen782:2147483647@localhost:5432/TP1_IDS"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route("/")
def hello_world():
    return "Hola Mundinho"

if __name__ == "__main__":
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host="127.0.0.1", port=8000, debug=True)