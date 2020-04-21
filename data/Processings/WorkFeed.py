import flask
from flask import render_template

from data import db_session
from data.works import Works

blueprint = flask.Blueprint('WorkFeed_api', __name__,
                            template_folder='data/Pages')
blueprint.secret_key = 'yandexlyceum_secret_key'


@blueprint.route('/workfeed')
def workfeed():
    return render_template()
    session = db_session.create_session()
    works = session.query(Works).filter(Works.is_private != True)
    return render_template('WorkFeed.html', news=works)
