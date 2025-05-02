from flask import Flask
from data import db_session
from data.users import User
from data.games_chess import GameChess


def add():
    db_session.global_init("/home/pashok/PycharmProjects/chess/db/data.db")
    db_sess = db_session.create_session()
    user = User()
    user.nickname = 'root'
    user.set_password('root')
    db_sess.add(user)
    user1 = User()
    user1.nickname = 'root2'
    user1.set_password('root2')
    db_sess.add(user1)
    db_sess.commit()


def remove():
    db_session.global_init("/home/pashok/PycharmProjects/chess/db/data.db")
    db_sess = db_session.create_session()
    db_sess.query(GameChess).delete()
    db_sess.commit()


if __name__ == '__main__':
    remove()
