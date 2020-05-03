from flask import jsonify
from flask_restful import abort, Resource, reqparse

from data import db_session
from data.users import User

parser = reqparse.RequestParser()
parser.add_argument('nickname')
parser.add_argument('name')
parser.add_argument('email')
parser.add_argument('status')


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, error=f"User {user_id} not found")


class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict(
            only=('nickname', 'name', 'email', 'status'))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, user_id):
        abort_if_user_not_found(user_id)
        args = parser.parse_args()
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        user.email = args['email']
        user.nickname = args['nickname']
        user.name = args['name']
        user.status = args['status']
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        user = session.query(User).all()
        return jsonify({'user': [item.to_dict(
            only=('nickname', 'name', 'email', 'status', 'id')) for item in user]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            nickname=args['nickname'],
            name=args['name'],
            email=args['email'],
            status=args['status']
        )
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})
