from flask import Flask, render_template, request, jsonify
from flask_login import LoginManager,  login_required, logout_user
from flask import make_response
from werkzeug.utils import redirect
from flask_restful import Api
from Engine import UsersListResource, UserResource
from data import db_session
from data.Processings.Register import reqister
from data.users import User
import datetime
from data.Processings.Login import login

app = Flask(__name__, template_folder='Pages')
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)

api.add_resource(UsersListResource, '/api/user')
api.add_resource(UserResource, '/api/user/<int:user_id>')

login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/SND.sqlite")
    app.run()


@login_manager.user_loader
def load_user(id):
    session = db_session.create_session()
    return session.query(User).get(id)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/')
def base():
    return render_template('base.html', title='SNAC')


@app.route('/login', methods=['GET', 'POST'])
def log():
    login()


@app.route('/register', methods=['GET', 'POST'])
def reqist():
    reqister()


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/sample_file_upload', methods=['POST', 'GET'])
def sample_file_upload():
    if request.method == 'GET':
        return f'''<!doctype html>
                        <html lang="en">
                          <head>
                            <meta charset="utf-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                            <title>Пример загрузки файла</title>
                          </head>
                          <body>
                            <h1>Загрузим файл</h1>
                            <form method="post" enctype="multipart/form-data">
                               <div class="form-group">
                                    <label for="photo">Выберите файл</label>
                                    <input type="file" class="form-control-file" id="photo" name="file">
                                </div>
                                <button type="submit" class="btn btn-primary">Отправить</button>
                            </form>
                          </body>
                        </html>'''
    elif request.method == 'POST':
        with open('static/upload_files/photo.jpg', 'wb') as p:
            p.write(request.files['file'].read())
        return "Форма отправлена"


if __name__ == '__main__':
    main()
