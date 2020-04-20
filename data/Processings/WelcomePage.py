import flask
from flask import render_template

blueprint = flask.Blueprint('welpage_api', __name__,
                            template_folder='data/Pages')
blueprint.secret_key = 'yandexlyceum_secret_key'


@blueprint.route('/', methods=['GET', 'POST'])
def welcome():
    return render_template('WelcomePage.html', title='SNAC', welcome_text1='Добро пожаловать в SNAC.',
                           welcome_text2='SNAC-это социальная сеть для художников всех уровней мастерстава.',
                           welcome_text3='На данный момент соцсеть является проектной работой и скорее',
                           welcome_text4='всего не будет подерживатся в будущем.')
