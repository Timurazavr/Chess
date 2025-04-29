import asyncio

from flask import Flask, request, redirect, jsonify, make_response, url_for
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


def replace_instances(text: str, lis: [str]):
    for i in lis:
        text = text.replace(i, '')
    return text


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/', methods=['GET', 'POST'])
def index():
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
    if current_user.is_authenticated:
        if not request.script_root:
            request.root_path = url_for('index', _external=True)
        db_sess = db_session.create_session()
        try:
            sess = db_sess.query(GameChess).filter(
                GameChess.white_id == current_user.id or GameChess.black_id == current_user.id).first()
            if sess.black_id != -1:
                return redirect(f'/session/{sess.id}')
        except Exception as e:
            if len(db_sess.query(GameChess).all()) != 0:
                session = db_sess.query(GameChess).first()
                session.black_id = current_user.id
                db_sess.commit()
                return redirect(f'/session/{session.id}')
            session = GameChess(
                white_id=current_user.id,
            )
            db_sess.add(session)
            db_sess.commit()
        return render_template('waiting.html')
    else:
        return redirect('/login')


@app.route('/check', methods=['GET'])
@login_required
def check():
    db_sess = db_session.create_session()
    session = db_sess.query(GameChess).filter(GameChess.white_id == current_user.id).first()
    if session.black_id == -1:
        return jsonify(start_game=False)
    enemy = db_sess.query(User).filter(User.id == session.black_id).first()
    return jsonify(start_game=True, session=session.id, enemy=enemy.nickname)


@app.route("/session/<session_id>", methods=['GET'])
def session(session_id):
    if current_user.is_authenticated:
        if not request.script_root:
            request.root_path = url_for('index', _external=True)
        return render_template('session.html', session_id=session_id)
    else:
        return redirect('/login')


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


@app.route('/test')
def test():
    if not request.script_root:
        request.root_path = url_for('index', _external=True)
    return render_template('session.html')


@app.route('/get_session_data/<session_id>')
def get_colour(session_id):
    if not request.script_root:
        request.root_path = url_for('index', _external=True)
    db_sess = db_session.create_session()
    colour = 'white' if db_sess.query(GameChess).filter(
        GameChess.id == session_id).first().white_id == current_user.id else 'black'
    board = replace_instances(db_sess.query(GameChess).filter(GameChess.id == session_id).first().board,
                              ['[', ']', ',', ' ', '\n'])[1:-1]
    print(colour)
    return jsonify(colour=colour, board=board)


@app.route('/get_board/<session_id>')
def get_board(session_id):
    if not request.script_root:
        request.root_path = url_for('index', _external=True)
    return jsonify(board=replace_instances(
        db_session.create_session().query(GameChess).filter(GameChess.id == session_id).first().board,
        ['[', ']', ',', ' ', '\n'])[1:-1])  # todo разобраться с асинхронностью


def main():
    db_session.global_init(PATH_TO_DB_FOLDER + "/data.db")
    app.run()


def rotate_board(board: [[], ]):
    return [board[i].reverse() for i in range(7, -1, -1)]


if __name__ == '__main__':
    main()
else:
    main()
