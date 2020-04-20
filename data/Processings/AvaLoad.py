import flask
from flask import render_template, request
from werkzeug.utils import redirect

from data import db_session
from data.users import User

blueprint = flask.Blueprint('avaload_api', __name__,
                            template_folder='data/Pages')
blueprint.secret_key = 'yandexlyceum_secret_key'


@blueprint.route('/sample_file_upload', methods=['POST', 'GET'])
def sample_file_upload():
    if request.method == 'GET':
        return render_template('AvaLoad.html')
    elif request.method == 'POST':
        with open('data/AvaPhotos/photo.jpg', 'wb') as p:
            p.write(request.files['file'].read())
        return redirect('/perspage')
