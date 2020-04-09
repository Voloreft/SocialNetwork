from os import abort

from flask import Flask, render_template, request
from flask_login import LoginManager, login_user, current_user, login_required, logout_user

from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired

from Engine import main
from data import db_session
from data.users import User
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['DEBUG'] = 'True'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
@app.route('/start')
def start():
    return render_template("start.html")


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


if __name__ == '__main__':
    main()
