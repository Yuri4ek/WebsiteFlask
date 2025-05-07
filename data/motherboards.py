import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class MotherBoards(SqlAlchemyBase):
    __tablename__ = 'motherboards'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    socket_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("sockets.id"))
    chipset = sqlalchemy.Column(sqlalchemy.String)
    memory_type_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("memory_types.id"))
    memory_slots = sqlalchemy.Column(sqlalchemy.Integer)
    memory_max = sqlalchemy.Column(sqlalchemy.Integer)
    m2_quantity = sqlalchemy.Column(sqlalchemy.Integer)
    pcie_type = sqlalchemy.Column(sqlalchemy.Integer)
    form_factor = sqlalchemy.Column(sqlalchemy.String)
    price_in_rubles = sqlalchemy.Column(sqlalchemy.Integer)

    socket = orm.relationship("Sockets")
    memory_type = orm.relationship("MemoryTypes")

    def get(self):
        return (self.id, self.name, self.socket_id, self.chipset, self.memory_type_id,
                self.memory_slots, self.memory_max, self.m2_quantity, self.pcie_type,
                self.form_factor, self.price_in_rubles)
