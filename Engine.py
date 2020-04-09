from flask import Flask

from data import db_session
from data.Processings import Login, Register

app = Flask(__name__)


def main():
    db_session.global_init("db/SND.sqlite")
    session = db_session.create_session()
    app.register_blueprint(Login.blueprint)
    app.register_blueprint(Register.blueprint)
    app.run()

