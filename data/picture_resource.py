from flask import jsonify
from flask_restful import abort, Resource, reqparse

from data import db_session
from data.pictures import Picture
from data.users import User

parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('picture_path', required=True)
# parser.add_argument('average_mark', required=True)
parser.add_argument('user_id', required=True)


def abort_if_picture_not_found(picture_id):
    session = db_session.create_session()
    picture = session.query(Picture).get(picture_id)
    if not picture:
        abort(404, error=f"Picture {picture_id} not found")


class PictureResource(Resource):
    def get(self, picture_id):
        abort_if_picture_not_found(picture_id)
        session = db_session.create_session()
        picture = session.query(Picture).get(picture_id)
        return jsonify({'picture': picture.to_dict(
            only=('title', 'picture_path', 'user_id'))})

    def delete(self, picture_id):
        abort_if_picture_not_found(picture_id)
        session = db_session.create_session()
        picture = session.query(Picture).get(picture_id)
        session.delete(picture)
        session.commit()
        return jsonify({'success': 'OK'})


class PicturesListResource(Resource):
    def get(self):
        session = db_session.create_session()
        picture = session.query(Picture).all()
        picture.reverse()
        return jsonify({'picture': [item.to_dict(
            only=('title', 'picture_path', 'user_id', 'id')) for item in picture]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        picture = Picture(title=args['title'],
                          picture_path=args['picture_path'],
                          user_id=args['user_id'])
        session.add(picture)
        session.commit()
        return jsonify({'success': 'OK'})
