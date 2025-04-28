import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class MemoryTypes(SqlAlchemyBase):
    __tablename__ = 'memory_types'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)

    motherboards = orm.relationship("MotherBoards",
                                    back_populates="memory_type")

    def get(self):
        return self.id, self.name
