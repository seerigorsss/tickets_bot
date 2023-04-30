import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Trips(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'trips'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    source_title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    target_title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    source_date = sqlalchemy.Column(sqlalchemy.DateTime)
    target_date = sqlalchemy.Column(sqlalchemy.DateTime)
    price = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    is_private = sqlalchemy.Column(sqlalchemy.Boolean, default=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('User')
