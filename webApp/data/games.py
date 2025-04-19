import sqlalchemy
# from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class GameKN(SqlAlchemyBase):
    __tablename__ = 'games'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    cross_id = sqlalchemy.Column(sqlalchemy.ForeignKey('users.id'))
    circle_id = sqlalchemy.Column(sqlalchemy.ForeignKey('users.id'))
    whose_turn = sqlalchemy.Column(sqlalchemy.String, default='cross')
    board = sqlalchemy.Column(sqlalchemy.String)
