import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase
from .users import User


class Picture(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'pictures'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    title = sqlalchemy.Column(sqlalchemy.String, default='Рисунок')
    likes = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    dislikes = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    user_list = sqlalchemy.Column(sqlalchemy.Integer, default='')
    picture_path = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    average_mark = sqlalchemy.Column(sqlalchemy.String)
    time_modified = sqlalchemy.Column(sqlalchemy.DateTime,
                                      default=datetime.datetime.now)

    user = orm.relation('User')
