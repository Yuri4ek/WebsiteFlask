import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Processors(SqlAlchemyBase):
    __tablename__ = 'processors'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    socket = sqlalchemy.Column(sqlalchemy.String)
    efficiency = sqlalchemy.Column(sqlalchemy.REAL)
    cores_threads = sqlalchemy.Column(sqlalchemy.String)
    release_year = sqlalchemy.Column(sqlalchemy.Integer)
    tdp = sqlalchemy.Column(sqlalchemy.Integer)
    price = sqlalchemy.Column(sqlalchemy.REAL)
    currency = sqlalchemy.Column(sqlalchemy.String)