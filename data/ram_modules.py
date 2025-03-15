import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class RamModules(SqlAlchemyBase):
    __tablename__ = 'ram_modules'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    memory_type_id = sqlalchemy.Column(sqlalchemy.Integer,
                                       sqlalchemy.ForeignKey(
                                           "memory_types.id"))
    price = sqlalchemy.Column(sqlalchemy.REAL)
    currency = sqlalchemy.Column(sqlalchemy.String)

    memory_type = orm.relationship("MemoryTypes")
