import os
from flask import Flask, render_template, request, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask import make_response
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from werkzeug.utils import redirect
from wtforms import PasswordField, StringField, SubmitField, BooleanField, FileField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from flask_restful import Api, abort
from requests import get, post, put
from data import db_session, picture_resource, user_resource, date_reduction
from data.pictures import Picture
from data.users import User
import datetime

app = Flask(__name__, template_folder='static/pages')
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)

api.add_resource(user_resource.UsersListResource, '/api/user')
api.add_resource(user_resource.UserResource, '/api/user/<int:user_id>')

api.add_resource(picture_resource.PicturesListResource, '/api/picture')
api.add_resource(picture_resource.PictureResource, '/api/picture/<int:picture_id>')

login_manager = LoginManager()
login_manager.init_app(app)


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class EditUserForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    nickname = StringField('Имя пользователя', validators=[DataRequired()])
    name = StringField('Ваше имя (оно будет использоватся в системных сообшениях и небудет разглашатся пользователям)',
                       validators=[DataRequired()])
    status = StringField('Ваш статус')
    submit = SubmitField('Сохранить изменения')


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    nickname = StringField('Имя пользователя', validators=[DataRequired()])
    name = StringField('Ваше имя (оно будет использоватся в системных сообшениях и небудет разглашатся пользователям)',
                       validators=[DataRequired()])
    submit = SubmitField('Зарегестрироваться')


class NewPostForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    photo = FileField('Фото', validators=[FileRequired()])
    submit = SubmitField('Выложить')


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
    if current_user.is_authenticated:
        return redirect('/feed_p_a')
    else:
        return render_template('start.html', title='SNAC')


@app.route('/feed_<sr>_<sub>', methods=['POST', 'GET'])
def feed(sr, sub):
    subs = current_user.followed
    pictures = get('http://localhost:5000/api/picture').json()['picture']
    ###
    for pic in pictures:
        a = datetime.datetime.strptime(pic['time_modified'], '%Y-%m-%d %H:%M')
        n = datetime.datetime.now()
        d = n - a
        pic['elapsed_time'] = date_reduction.reduct_date(d)
    picturs = list()
    ###
    if sub == 's':
        for pic in pictures:
            if str(pic['user_id']) in subs:
                picturs.append(pic)
        pictures = picturs
    ##3
    if sr == 'n':
        pictures.sort(key=lambda new: new['id'], reverse=True)
        return render_template('workfeed.html', title='Лента работ',
                               pictures=pictures)
    elif sr == 'o':
        pictures.sort(key=lambda new: new['id'])
        return render_template('workfeed.html', title='Лента работ',
                               pictures=pictures)
    elif sr == 'p':
        pictures.sort(key=lambda popular: popular['likes'] - popular['dislikes'] * 0.9, reverse=True)
        return render_template('workfeed.html', title='Лента работ',
                               pictures=pictures)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            if not os.path.exists(f'static/upload_files/{current_user.id}'):
                os.mkdir(f'static/upload_files/{current_user.id}')
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form, message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            nickname=form.nickname.data,
            name=form.name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/file_upload', methods=['POST', 'GET'])
@login_required
def sample_file_upload():
    if request.method == 'GET':
        return render_template('AvaLoad.html', title='Загрузка файла')
    elif request.method == 'POST':
        with open(f'static/AvaPhotos/id{current_user.id}.jpg', 'wb') as p:
            p.write(request.files['file'].read())
        if not current_user.ava_have:
            session = db_session.create_session()
            ed_user = session.query(User).filter_by(id=current_user.id).one()
            ed_user.ava_have = True
            session.add(ed_user)
            session.commit()
        return redirect('/index')


@app.route('/edit', methods=['POST', 'GET'])
@login_required
def edit():
    form = EditUserForm()
    if request.method == 'GET':
        user = get(f'http://localhost:5000/api/user/{current_user.id}').json()
        form.name.data = user['user']['name']
        form.nickname.data = user['user']['nickname']
        form.email.data = user['user']['email']
        form.status.data = user['user']['status']

    if form.validate_on_submit():
        put(f'http://localhost:5000/api/user/{current_user.id}',
            json={'email': form.email.data,
                  'name': form.name.data,
                  'nickname': form.nickname.data,
                  'status': form.status.data}).json()
        return render_template('index.html', title=current_user.nickname)
    return render_template('Edit_user.html', title='Редактрование', form=form)


@app.route('/index')
@login_required
def index():
    pictures = get(f'http://127.0.0.1:5000/api/user/{current_user.id}').json()['user']['picture']
    followed = 0
    followers = 0
    if current_user.followed:
        followed = len([i for i in current_user.followed.split(';') if i])
    if current_user.followers:
        followers = len([i for i in current_user.followers.split(';') if i])
    for pic in pictures:
        a = datetime.datetime.strptime(pic['time_modified'], '%Y-%m-%d %H:%M')
        n = datetime.datetime.now()
        d = n - a
        pic['elapsed_time'] = date_reduction.reduct_date(d)
    return render_template('index.html', title=current_user.nickname, pictures=pictures, followed=followed, followers=followers)


@app.route('/new_post', methods=['POST', 'GET'])
@login_required
def new_post():
    form = NewPostForm()
    if form.validate_on_submit():
        iden = 1
        p = get('http://localhost:5000/api/picture').json()
        if p['picture']:
            iden = p['picture'][-1]['id'] + 1

        post('http://localhost:5000/api/picture', json={
            'title': form.title.data,
            'user_id': current_user.id,
            'picture_path': f'static/upload_files/{current_user.id}/{iden}.jpg'
        })
        picture = form.photo.data
        picture.save(f'static/upload_files/{current_user.id}/{iden}.jpg')
        return redirect('/')
    return render_template('newpost.html', title='Новый пост', form=form)


@app.route('/post_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def posts_delete(id):
    session = db_session.create_session()
    news = session.query(Picture).filter(Picture.id == id,
                                         Picture.user == current_user).first()
    if news:
        session.delete(news)
        session.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/index_users_<user_id>')
@login_required
def index_users(user_id):
    user = get(f'http://127.0.0.1:5000/api/user/{user_id}').json()['user']
    pictures = get(f'http://127.0.0.1:5000/api/user/{user_id}').json()['user']['picture']
    pictures.reverse()
    return render_template('index_users.html', title=user['nickname'], user=user, pictures=pictures)


if __name__ == '__main__':
    main()
