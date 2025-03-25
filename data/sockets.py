import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Sockets(SqlAlchemyBase):
    __tablename__ = 'sockets'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)

    processors = orm.relationship("Processors", back_populates="socket")
    motherboards = orm.relationship("MotherBoards", back_populates="socket")
    cooling_systems = orm.relationship("CoolingSystems",
                                       back_populates="socket")
