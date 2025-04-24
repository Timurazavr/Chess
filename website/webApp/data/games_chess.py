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
    board = sqlalchemy.Column(sqlalchemy.String, default=str([['BR', 'BN', 'BB', 'BQ', 'BK', 'BB', 'BN', 'BR'],
                                                              ['BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP'],
                                                              ['--', '--', '--', '--', '--', '--', '--', '--'],
                                                              ['--', '--', '--', '--', '--', '--', '--', '--'],
                                                              ['--', '--', '--', '--', '--', '--', '--', '--'],
                                                              ['--', '--', '--', '--', '--', '--', '--', '--'],
                                                              ['WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP'],
                                                              ['WR', 'WN', 'WB', 'WQ', 'WK', 'WB', 'WN', 'WR']
                                                              ]))
