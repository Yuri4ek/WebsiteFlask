import sqlalchemy
from .db_session import SqlAlchemyBase


class AirCoolers(SqlAlchemyBase):
    __tablename__ = 'air_coolers'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    tdp = sqlalchemy.Column(sqlalchemy.Integer)
    price_in_rubles = sqlalchemy.Column(sqlalchemy.Integer)

    def get(self):
        return self.id, self.name, self.tdp, self.price_in_rubles
