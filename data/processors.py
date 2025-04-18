import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Processors(SqlAlchemyBase):
    __tablename__ = 'processors'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    socket_id = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey("sockets.id"))
    efficiency = sqlalchemy.Column(sqlalchemy.REAL)
    cores_threads = sqlalchemy.Column(sqlalchemy.String)
    release_year = sqlalchemy.Column(sqlalchemy.Integer)
    tdp = sqlalchemy.Column(sqlalchemy.Integer)
    price = sqlalchemy.Column(sqlalchemy.REAL)
    currency = sqlalchemy.Column(sqlalchemy.String)

    socket = orm.relationship("Sockets")

    def get(self):
        return (self.id, self.name, self.socket_id, self.efficiency,
                self.cores_threads, self.release_year, self.tdp, self.price,
                self.currency)
