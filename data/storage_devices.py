import sqlalchemy
from .db_session import SqlAlchemyBase


class StorageDevices(SqlAlchemyBase):
    __tablename__ = 'storage_devices'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    storage_type = sqlalchemy.Column(sqlalchemy.String)
    capacity_gb = sqlalchemy.Column(sqlalchemy.Integer)
    price = sqlalchemy.Column(sqlalchemy.REAL)
    currency = sqlalchemy.Column(sqlalchemy.String)
