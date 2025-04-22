import sqlalchemy
from .db_session import SqlAlchemyBase


class Forum(SqlAlchemyBase):
    __tablename__ = 'forum'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    content = sqlalchemy.Column(sqlalchemy.Text, nullable=False)

    def __repr__(self):
        return f'<Forum {self.title}>'