import sqlalchemy
# from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Game(SqlAlchemyBase):
    __tablename__ = 'games'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    white_id = sqlalchemy.Column(sqlalchemy.ForeignKey('users.id'))
    black_id = sqlalchemy.Column(sqlalchemy.ForeignKey('users.id'))
    whose_turn = sqlalchemy.Column(sqlalchemy.String, default='White')
    board = sqlalchemy.Column(sqlalchemy.String)
