import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class User_tg(SqlAlchemyBase):
    __tablename__ = "users_tg"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    last_message_id = sqlalchemy.Column(sqlalchemy.Integer)
    session_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("games.id")
    )
    session = orm.relationship("GameChess", backref="users_tg")
