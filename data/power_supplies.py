import sqlalchemy
from .db_session import SqlAlchemyBase


class PowerSupplies(SqlAlchemyBase):
    __tablename__ = 'power_supplies'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    power = sqlalchemy.Column(sqlalchemy.Integer)
    price_in_rubles = sqlalchemy.Column(sqlalchemy.Integer)

    def get(self):
        return self.id, self.name, self.power, self.price_in_rubles