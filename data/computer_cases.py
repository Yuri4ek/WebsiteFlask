import sqlalchemy
from .db_session import SqlAlchemyBase


class ComputerCases(SqlAlchemyBase):
    __tablename__ = 'computer_cases'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    form_factor = sqlalchemy.Column(sqlalchemy.String)
    price = sqlalchemy.Column(sqlalchemy.REAL)
    currency = sqlalchemy.Column(sqlalchemy.String)
