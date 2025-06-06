import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Sockets(SqlAlchemyBase):
    __tablename__ = 'sockets'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)

    processors = orm.relationship("Processors", back_populates="socket")

    def get(self):
        return [self.id, self.name]
