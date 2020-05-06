from flask import jsonify
from flask_restful import abort, Resource, reqparse

from . import db_session
from .pictures import Picture
from .users import User


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
            only=(
                'title', 'picture_path', 'user_id', 'user.nickname', 'user.ava_have', 'likes', 'dislikes',
                'user_list'))})

    def delete(self, picture_id):
        abort_if_picture_not_found(picture_id)
        session = db_session.create_session()
        picture = session.query(Picture).get(picture_id)
        session.delete(picture)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, picture_id):
        abort_if_picture_not_found(picture_id)

        parser = reqparse.RequestParser()
        parser.add_argument('likes')
        parser.add_argument('dislikes')
        parser.add_argument('user_list')
        args = parser.parse_args()

        session = db_session.create_session()
        picture = session.query(Picture).get(picture_id)
        user_id = args['user_list'].split('_')[0]

        if int(args['likes']) == 1 and f'{user_id}_d' in picture.user_list:
            picture.user_list = picture.user_list.replace(f'{user_id}_d', '')
            picture.user_list += args['user_list'] + ' '
            picture.likes += 1
            picture.dislikes -= 1
        elif int(args['likes']) == 1 and f'{user_id}_l' not in picture.user_list:
            picture.user_list += args['user_list'] + ' '
            picture.likes += 1
        elif int(args['likes']) == 1 and f'{user_id}_l' in picture.user_list:
            picture.user_list = picture.user_list.replace(f'{user_id}_l', '')
            picture.likes -= 1

        if int(args['dislikes']) == 1 and f'{user_id}_l' in picture.user_list:
            picture.user_list = picture.user_list.replace(f'{user_id}_l', '')
            picture.user_list += args['user_list'] + ' '
            picture.dislikes += 1
            picture.likes -= 1
            print(picture.user_list)
        elif int(args['dislikes']) == 1 and f'{user_id}_d' not in picture.user_list:
            picture.user_list += args['user_list'] + ' '
            picture.dislikes += 1
            print(picture.user_list)
        elif int(args['dislikes']) == 1 and f'{user_id}_d' in picture.user_list:
            picture.user_list = picture.user_list.replace(f'{user_id}_d', '')
            picture.dislikes -= 1
            print(picture.user_list)

        session.commit()
        return jsonify({'success': 'OK'})


class PicturesListResource(Resource):
    def get(self):
        session = db_session.create_session()
        picture = session.query(Picture).all()
        return jsonify({'picture': [item.to_dict(
            only=('title', 'picture_path', 'user_id', 'id', 'user.nickname', 'user.ava_have', 'likes', 'dislikes',
                  'user_list')) for
            item in picture]})

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', required=True)
        parser.add_argument('picture_path', required=True)
        # parser.add_argument('average_mark', required=True)
        parser.add_argument('user_id', required=True)
        args = parser.parse_args()

        session = db_session.create_session()
        picture = Picture(title=args['title'],
                          picture_path=args['picture_path'],
                          user_id=args['user_id'])
        session.add(picture)
        session.commit()
        return jsonify({'success': 'OK'})
