import sqlalchemy
from .db_session import SqlAlchemyBase


class ComputerCases(SqlAlchemyBase):
    __tablename__ = 'computer_cases'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    image_path = sqlalchemy.Column(sqlalchemy.String)
    form_factor = sqlalchemy.Column(sqlalchemy.String)
    price = sqlalchemy.Column(sqlalchemy.REAL)
    currency = sqlalchemy.Column(sqlalchemy.String)

    def get(self):
        return self.id, self.name, self.form_factor, self.price, self.currency
