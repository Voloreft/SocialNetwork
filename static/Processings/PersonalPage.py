import flask
from flask import render_template
from flask_login import current_user

blueprint = flask.Blueprint('personalpage_api', __name__,
                            template_folder='data/Pages')
blueprint.secret_key = 'yandexlyceum_secret_key'


@blueprint.route('/perspage')
def personalpage():
    return render_template('index.html', title=current_user.nickname)
    #return render_template('PersonalPage.html')
