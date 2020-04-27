import flask
from flask import render_template, request
from werkzeug.utils import redirect
from flask_login import current_user

blueprint = flask.Blueprint('avaload_api', __name__,
                            template_folder='data/Pages')
blueprint.secret_key = 'yandexlyceum_secret_key'


@blueprint.route('/sample_file_upload', methods=['POST', 'GET'])
def sample_file_upload():
    if request.method == 'GET':
        return render_template('AvaLoad.html')
    elif request.method == 'POST':
        with open(f'static/AvaPhotos/id{current_user.id}.jpg', 'wb') as p:
            p.write(request.files['file'].read())
        return redirect('/perspage')
