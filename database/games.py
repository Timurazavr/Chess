import sqlalchemy
from .db_session import SqlAlchemyBase

# from sqlalchemy import orm


class Game(SqlAlchemyBase):
    __tablename__ = "games"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    white_id = sqlalchemy.Column(sqlalchemy.Integer)
    black_id = sqlalchemy.Column(sqlalchemy.Integer, default=-1)
    board = sqlalchemy.Column(
        sqlalchemy.String,
        default=str(["rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"]),
    )
    is_finished = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
