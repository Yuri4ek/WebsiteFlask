import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Configurations(SqlAlchemyBase):
    __tablename__ = 'configurations'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    components = sqlalchemy.Column(sqlalchemy.PickleType)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('Users')
