import sqlalchemy
from .db_session import SqlAlchemyBase


class Videocards(SqlAlchemyBase):
    __tablename__ = 'videocards'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    release_year = sqlalchemy.Column(sqlalchemy.Integer)
    tdp = sqlalchemy.Column(sqlalchemy.Integer)
    memory_capacity = sqlalchemy.Column(sqlalchemy.Integer)
    pcie_type = sqlalchemy.Column(sqlalchemy.Integer)
    price_in_rubles = sqlalchemy.Column(sqlalchemy.Integer)

    def get(self):
        return (self.id, self.name, self.tdp, self.release_year,
                self.memory_capacity, self.pcie_type, self.price_in_rubles)
