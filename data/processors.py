import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Processors(SqlAlchemyBase):
    __tablename__ = 'processors'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    release_year = sqlalchemy.Column(sqlalchemy.Integer)
    socket_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("sockets.id"))
    cores = sqlalchemy.Column(sqlalchemy.Integer)
    threads = sqlalchemy.Column(sqlalchemy.Integer)
    processor_frequency = sqlalchemy.Column(sqlalchemy.Integer)
    tdp = sqlalchemy.Column(sqlalchemy.Integer)
    memory_type_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("memory_types.id"))
    memory_frequency = sqlalchemy.Column(sqlalchemy.Integer)
    pcie_type = sqlalchemy.Column(sqlalchemy.Integer)
    price_in_rubles = sqlalchemy.Column(sqlalchemy.REAL)

    socket = orm.relationship("Sockets")
    memory_type = orm.relationship("MemoryTypes")

    def get(self):
        return (self.id, self.name, self.release_year, self.socket_id, self.cores, self.threads,
                self.processor_frequency, self.tdp, self.memory_type_id, self.memory_frequency,
                self.pcie_type, self.price_in_rubles)
