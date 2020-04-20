import flask
from flask import render_template

blueprint = flask.Blueprint('personalpage_api', __name__,
                            template_folder='data/Pages')
blueprint.secret_key = 'yandexlyceum_secret_key'


@blueprint.route('/perspage')
def personalpage():
    return render_template('PersonalPage.html')
