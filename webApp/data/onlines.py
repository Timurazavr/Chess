import sqlalchemy
# from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Online(SqlAlchemyBase):
    __tablename__ = 'onlines'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    id_online = sqlalchemy.Column(sqlalchemy.ForeignKey('users.id'), nullable=True)
