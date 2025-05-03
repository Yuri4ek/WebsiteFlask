import sqlalchemy
from sqlalchemy.orm import relationship
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Forum(SqlAlchemyBase):
    __tablename__ = 'forum'  # Была ошибка: должно быть tablename

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    content = sqlalchemy.Column(sqlalchemy.Text, nullable=False)

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))  # Связь с User
    user = orm.relationship("User", back_populates="forums")  # Обратная связь

    comments = relationship("Comment", back_populates="forum")  # Предположим, что модель Comment уже есть

    def __repr__(self):
        return f'<Forum {self.title}>'