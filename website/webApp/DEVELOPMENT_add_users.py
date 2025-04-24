from flask import Flask
from data import db_session
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("../db/users.db")
    db_sess = db_session.create_session()
    app.run()
    user = User()
    user.nickname = "Ridley"
    user.hashed_password = "cap"
    db_sess.add(user)

    user = User()
    user.nickname = "andrey"
    user.hashed_password = "zalupa"
    db_sess.add(user)

    user = User()
    user.nickname = "haahah"
    user.hashed_password = "fyjuk"
    db_sess.add(user)

    user = User()
    user.nickname = "ROOT"
    user.hashed_password = "ROOT"
    db_sess.add(user)

    db_sess.commit()


if __name__ == '__main__':
    main()
