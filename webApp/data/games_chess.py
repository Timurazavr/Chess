import sqlalchemy
# from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class GameChess(SqlAlchemyBase):
    __tablename__ = 'games'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    white_id = sqlalchemy.Column(sqlalchemy.Integer)
    black_id = sqlalchemy.Column(sqlalchemy.Integer, default=-1)
    whose_turn = sqlalchemy.Column(sqlalchemy.String, default='White')
    board = sqlalchemy.Column(sqlalchemy.String, default=str([['WR', 'WN', 'WB', 'WQ', 'WK', 'WB', 'WN', 'WR'],
                                                              ['WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP'],
                                                              ['--', '--', '--', '--', '--', '--', '--', '--'],
                                                              ['--', '--', '--', '--', '--', '--', '--', '--'],
                                                              ['--', '--', '--', '--', '--', '--', '--', '--'],
                                                              ['--', '--', '--', '--', '--', '--', '--', '--'],
                                                              ['BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP'],
                                                              ['BR', 'BN', 'BB', 'BQ', 'BK', 'BB', 'BN', 'BR']]))
