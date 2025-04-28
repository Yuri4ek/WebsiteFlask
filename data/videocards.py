import sqlalchemy
from .db_session import SqlAlchemyBase


class Videocards(SqlAlchemyBase):
    __tablename__ = 'videocards'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    efficiency = sqlalchemy.Column(sqlalchemy.REAL)
    release_year = sqlalchemy.Column(sqlalchemy.Integer)
    tdp = sqlalchemy.Column(sqlalchemy.Integer)
    price = sqlalchemy.Column(sqlalchemy.REAL)
    currency = sqlalchemy.Column(sqlalchemy.String)

    def get(self):
        return (self.id, self.name, self.efficiency, self.release_year,
                self.tdp, self.price, self.currency)
