from flask import Flask, request, redirect, jsonify, make_response
from flask import render_template
from data import db_session
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from data.users import User
from data.games_chess import GameChess
from forms.register import RegisterForm
from forms.login import LoginForm
from forms.start_game import StartGameForm

# for linux absolute path
# for windows relative path
PATH_TO_DB_FOLDER = '/home/pashok/PycharmProjects/chess/db'
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/', methods=['GET', 'POST'])
def start():
    if current_user.is_authenticated:
        form = StartGameForm()
        if form.validate_on_submit():
            return redirect('/waiting_for_players')
        return render_template('start_game.html', form=form)
    else:
        return redirect('/login')


@app.route('/waiting_for_players', methods=['GET'])
@login_required
def waiting():
    # db_sess = db_session.create_session()
    # if not db_sess.query(GameChess).filter(
    #         GameChess.white_id == current_user.id or GameChess.black_id == current_user.id).first():
    #     if len(db_sess.query(GameChess).all()) != 0:
    #         session = db_sess.query(GameChess).first()
    #         session.black_id = current_user.id
    #         db_sess.commit()
    #         return redirect(f'/session/{session.id}')
    #     session = GameChess(
    #         white_id=current_user.id,
    #     )
    #     db_sess.add(session)
    #     db_sess.commit()
    return render_template('waiting.html')


@app.route('/check', methods=['GET'])
@login_required
# def check():
#     db_sess = db_session.create_session()
#     session = db_sess.query(GameChess).filter(GameChess.white_id == current_user.id).first()
#     if session.black_id == -1:
#         return jsonify(start_game=False)
#     return jsonify(start_game=True, session=session.id)
def check():
    return jsonify(start_game=False)


@app.route("/session/<session_id>", methods=['GET'])
def cookie_test(session_id):
    return 0


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.nickname == form.nickname.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            nickname=form.nickname.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.nickname == form.nickname.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init(PATH_TO_DB_FOLDER + "/users.db")
    app.run()


def rotate_board(board: [[], ]):
    return [board[i].reverse() for i in range(7, -1, -1)]


if __name__ == '__main__':
    main()
else:
    main()
