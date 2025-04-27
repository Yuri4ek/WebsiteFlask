from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .db_session import SqlAlchemyBase


class Comment(SqlAlchemyBase):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    forum_id = Column(Integer, ForeignKey('forum.id'))
    content = Column(String, nullable=False)

    forum = relationship("Forum", back_populates="comments")
