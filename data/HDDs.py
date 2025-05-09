import sqlalchemy
from .db_session import SqlAlchemyBase


class HDDs(SqlAlchemyBase):
    __tablename__ = 'HHDs'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    capacity_gb = sqlalchemy.Column(sqlalchemy.Integer)
    price_in_rubles = sqlalchemy.Column(sqlalchemy.Integer)

    def get(self):
        return self.id, self.name, self.capacity_gb,  self.price_in_rubles
