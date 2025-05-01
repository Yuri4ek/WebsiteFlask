import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Configuration(SqlAlchemyBase):
    __tablename__ = 'configurations'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    image_path = sqlalchemy.Column(sqlalchemy.String)
    components = sqlalchemy.Column(sqlalchemy.PickleType)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('Users')
