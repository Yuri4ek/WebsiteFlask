import sqlalchemy
from .db_session import SqlAlchemyBase


class SSDs(SqlAlchemyBase):
    __tablename__ = 'SSDs'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    m2 = sqlalchemy.Column(sqlalchemy.Boolean)
    capacity_gb = sqlalchemy.Column(sqlalchemy.Integer)
    price_in_rubles = sqlalchemy.Column(sqlalchemy.Integer)

    def get(self):
        return [self.id, self.name, self.m2, self.capacity_gb,  self.price_in_rubles]
