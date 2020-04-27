from flask import Flask, jsonify
from flask_login import LoginManager, login_required, logout_user
from flask import make_response
from werkzeug.utils import redirect
from flask_restful import Api
from Engine import UsersListResource, UserResource, PicturesListResource, PictureResource
from data import db_session
from static.Processings import WelcomePage, PersonalPage, AvaLoad, Login, Register
from data.users import User
import datetime



app = Flask(__name__, template_folder='static/Pages')
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)

api.add_resource(UsersListResource, '/api/user')
api.add_resource(UserResource, '/api/user/<int:user_id>')

api.add_resource(PicturesListResource, '/api/picture')
api.add_resource(PictureResource, '/api/picture<int:picture_id>')

login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/SND.sqlite")
    app.register_blueprint(Login.blueprint)
    app.register_blueprint(PersonalPage.blueprint)
    app.register_blueprint(Register.blueprint)
    app.register_blueprint(AvaLoad.blueprint)
    app.register_blueprint(WelcomePage.blueprint)
    app.run(debug=False)


@login_manager.user_loader
def load_user(id):
    session = db_session.create_session()
    return session.query(User).get(id)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    main()
