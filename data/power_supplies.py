import sqlalchemy
from .db_session import SqlAlchemyBase


class PowerSupplies(SqlAlchemyBase):
    __tablename__ = 'power_supplies'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    form_factor = sqlalchemy.Column(sqlalchemy.String)
    power = sqlalchemy.Column(sqlalchemy.Integer)
    price = sqlalchemy.Column(sqlalchemy.REAL)
    currency = sqlalchemy.Column(sqlalchemy.String)
