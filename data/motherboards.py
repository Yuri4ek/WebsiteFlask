import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Processors(SqlAlchemyBase):
    __tablename__ = 'motherboards'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    socket = sqlalchemy.Column(sqlalchemy.String)
    memory_type = sqlalchemy.Column(sqlalchemy.String)
    m2_support = sqlalchemy.Column(sqlalchemy.Boolean)
    form_factor = sqlalchemy.Column(sqlalchemy.String)
    price = sqlalchemy.Column(sqlalchemy.REAL)
    currency = sqlalchemy.Column(sqlalchemy.String)