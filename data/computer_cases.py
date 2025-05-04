import sqlalchemy
from .db_session import SqlAlchemyBase


class ComputerCases(SqlAlchemyBase):
    __tablename__ = 'computer_cases'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    price_in_rubles = sqlalchemy.Column(sqlalchemy.Integer)

    def get(self):
        return self.id, self.name, self.price_in_rubles
