import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class RamModules(SqlAlchemyBase):
    __tablename__ = 'ram_modules'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    capacity_gb = sqlalchemy.Column(sqlalchemy.Integer)
    frequency = sqlalchemy.Column(sqlalchemy.Integer)
    memory_type_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("memory_types.id"))
    price_in_rubles = sqlalchemy.Column(sqlalchemy.Integer)

    memory_type = orm.relationship("MemoryTypes")

    def get(self):
        return [self.id, self.name, self.capacity_gb, self.frequency, self.memory_type_id, self.price_in_rubles]
