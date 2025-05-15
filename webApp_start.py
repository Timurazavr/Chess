import json

from flask import Flask, request, redirect, jsonify, url_for
from flask import render_template
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    current_user,
    login_required,
)
from database import db_session
from database.users import User
from database.games_chess import GameChess
from webApp.forms.register import RegisterForm
from webApp.forms.login import LoginForm
from game_logic.chess_logic import Chess
from os.path import join
import sys

# for linux absolute path
# for windows relative path
CONFIG = json.load(open("config.json", "r"))
if sys.platform.startswith("win"):
    PATH_TO_DB_FOLDER = CONFIG["PATH_TO_CHESS_FOLDER_WIN"]
else:
    PATH_TO_DB_FOLDER = CONFIG["PATH_TO_CHESS_FOLDER"]
app = Flask(
    __name__,
    template_folder=join("webApp", "templates"),
    static_folder=join("webApp", "static"),
)
# IMPORTANT SECRET KEY
app.config["SECRET_KEY"] = CONFIG["SECRET_KEY"]

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
<<<<<<< HEAD
<<<<<<< HEAD
    usr = db_sess.get(User_web, user_id)
=======
    usr = db_sess.query(User).get(user_id)
>>>>>>> origin/master
=======
    usr = db_sess.query(User).get(user_id)
>>>>>>> parent of b28b61c (the raw final version)
    db_sess.close()
    return usr


<<<<<<< HEAD
@app.route("/", defaults={"message": None})
@app.route("/<string:message>", methods=["GET", "POST"])
def index(message):
    if current_user.is_authenticated:
        if not request.script_root:
            request.root_path = url_for("index", _external=True)
        if message == "error":
            return render_template("start_game.html", message="Some error has floated")
        return render_template("start_game.html", message="")
    else:
        return redirect("/login")


@app.route("/waiting_for_players", methods=["GET"])
=======
@app.route('/', defaults={'message': None})
@app.route('/<string:message>', methods=['GET', 'POST'])
def index(message):
    if current_user.is_authenticated:
        if not request.script_root:
            request.root_path = url_for('index', _external=True)
        if message == 'error':
            return render_template('start_game.html', message='Some error has floated')
        return render_template('start_game.html', message='')
    else:
        return redirect('/login')


@app.route('/waiting_for_players', methods=['GET'])
>>>>>>> origin/master
@login_required
def waiting():
    if current_user.is_authenticated:
        if not request.script_root:
<<<<<<< HEAD
            request.root_path = url_for("index", _external=True)
        db_sess = db_session.create_session()
        try:
            sess = (
                db_sess.query(GameChess)
                .filter(
                    (
                        (GameChess.white_id == current_user.id)
                        | (GameChess.black_id == current_user.id)
                    ),
                    GameChess.is_finished == 0,
                )
                .first()
            )
            if not sess:
                raise Exception
            if sess.black_id == -2:
                return render_template("waiting.html")
            elif sess.black_id == -1:
                raise Exception
            else:
                return redirect(f"/session/{sess.id}")
        except Exception as e:
            if (
                len(
                    db_sess.query(GameChess)
                    .filter(GameChess.black_id == -1, GameChess.is_finished == 0)
                    .all()
                )
                != 0
            ):
                game = (
                    db_sess.query(GameChess)
                    .filter(GameChess.black_id == -1, GameChess.is_finished == 0)
                    .first()
                )
                game.black_id = current_user.id
                db_sess.commit()
                return redirect(f"/session/{game.id}")
            game = GameChess(white_id=current_user.id)
            db_sess.add(game)
            db_sess.commit()
        db_sess.close()
        return render_template("waiting.html")
    else:
        return redirect("/login")


@app.route("/check", methods=["GET"])
@login_required
def check():
    db_sess = db_session.create_session()
    session = (
        db_sess.query(GameChess)
        .filter(GameChess.white_id == current_user.id, GameChess.is_finished == 0)
        .first()
    )
    if not session:
        return jsonify(legit=False)
    if session.black_id in [-2, -1]:
        return jsonify(
            legit=True, start_game=False, black_id=session.black_id, session=session.id
        )
    enemy = db_sess.query(User).filter(User.id == session.black_id).first()
    db_sess.close()
    return jsonify(
        legit=True, start_game=True, session=session.id, enemy=enemy.nickname
    )


@app.route("/session/<session_id>", methods=["GET"])
def session(session_id):
    if current_user.is_authenticated:
        if not request.script_root:
            request.root_path = url_for("index", _external=True)
        return render_template("session.html", session_id=session_id)
    else:
        return redirect("/login")


@app.route("/way_to_play/<string:way>", methods=["GET"])
def way_to_play(way: str):
    if current_user.is_authenticated:
        if not request.script_root:
            request.root_path = url_for("index", _external=True)
        if way == "random":
            return redirect("/waiting_for_players")
        elif way.isnumeric():
            db_sess = db_session.create_session()
            try:
                sess = (
                    db_sess.query(GameChess)
                    .filter(GameChess.id == int(way), GameChess.is_finished == 0)
                    .first()
                )
                if not sess:
                    raise Exception
                if sess.black_id == -2:
                    sess.black_id = current_user.id
                    db_sess.commit()
                    db_sess.close()
                    return redirect(f"/session/{int(way)}")
=======
            request.root_path = url_for('index', _external=True)
        db_sess = db_session.create_session()
        try:
            sess = db_sess.query(GameChess).filter(((GameChess.white_id == current_user.id) | (GameChess.black_id == current_user.id)), GameChess.is_finished == 0).first()
            if not sess:
                raise Exception
            if sess.black_id == -2:
                return render_template('waiting.html')
            elif sess.black_id == -1:
                raise Exception
            else:
                return redirect(f'/session/{sess.id}')
        except Exception as e:
            if len(db_sess.query(GameChess).filter(GameChess.black_id == -1, GameChess.is_finished == 0).all()) != 0:
                game = db_sess.query(GameChess).filter(GameChess.black_id == -1, GameChess.is_finished == 0).first()
                game.black_id = current_user.id
                db_sess.commit()
                return redirect(f'/session/{game.id}')
            game = GameChess(white_id=current_user.id)
            db_sess.add(game)
            db_sess.commit()
        db_sess.close()
        return render_template('waiting.html')
    else:
        return redirect('/login')


@app.route('/check', methods=['GET'])
@login_required
def check():
    db_sess = db_session.create_session()
    session = db_sess.query(GameChess).filter(GameChess.white_id == current_user.id, GameChess.is_finished == 0).first()
    if not session:
        return jsonify(legit=False)
    if session.black_id in [-2, -1]:
        return jsonify(legit=True, start_game=False, black_id=session.black_id, session=session.id)
    enemy = db_sess.query(User).filter(User.id == session.black_id).first()
    db_sess.close()
    return jsonify(legit=True, start_game=True, session=session.id, enemy=enemy.nickname)


@app.route("/session/<session_id>", methods=['GET'])
def session(session_id):
    if current_user.is_authenticated:
        if not request.script_root:
            request.root_path = url_for('index', _external=True)
        return render_template('session.html', session_id=session_id)
    else:
        return redirect('/login')


@app.route("/way_to_play/<string:way>", methods=['GET'])
def way_to_play(way: str):
    if current_user.is_authenticated:
        if not request.script_root:
            request.root_path = url_for('index', _external=True)
        if way == 'random':
            return redirect('/waiting_for_players')
        elif way.isnumeric():
            db_sess = db_session.create_session()
            try:
                sess = db_sess.query(GameChess).filter(GameChess.id == int(way), GameChess.is_finished == 0).first()
                if not sess:
                    raise Exception
                if sess.black_id == -2:
                    sess.black_id = current_user.id
                    db_sess.commit()
                    db_sess.close()
                    return redirect(f'/session/{int(way)}')
>>>>>>> origin/master
                else:
                    raise Exception
            except Exception:
                db_sess.close()
<<<<<<< HEAD
                return render_template(
                    "start_game.html", message="Неправильный id игры"
                )
        elif way == "create":
            db_sess = db_session.create_session()
<<<<<<< HEAD
            obj = Game(white_id=current_user.id)
=======
                return render_template('start_game.html', message='Неправильный id игры')
        elif way == 'create':
            db_sess = db_session.create_session()
            obj = GameChess(white_id=current_user.id)
>>>>>>> origin/master
=======
            obj = GameChess(white_id=current_user.id)
>>>>>>> parent of b28b61c (the raw final version)
            obj.black_id = -2
            db_sess.add(obj)
            db_sess.commit()
            db_sess.close()
<<<<<<< HEAD
        return redirect(f"/waiting_for_players")
    else:
        return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
=======
        return redirect(f'/waiting_for_players')
    else:
        return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
>>>>>>> origin/master
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
<<<<<<< HEAD
            return render_template(
                "register.html",
                title="Регистрация",
                form=form,
                message="Пароли не совпадают",
            )
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.nickname == form.nickname.data).first():
            return render_template(
                "register.html",
                title="Регистрация",
                form=form,
                message="Такой пользователь уже есть",
            )
<<<<<<< HEAD
        user = User_web(nickname=form.nickname.data)
=======
            return render_template('register.html', title='Регистрация', form=form, message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.nickname == form.nickname.data).first():
            return render_template('register.html', title='Регистрация', form=form, message="Такой пользователь уже есть")
        user = User(nickname=form.nickname.data)
>>>>>>> origin/master
=======
        user = User(nickname=form.nickname.data)
>>>>>>> parent of b28b61c (the raw final version)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        db_sess.close()
<<<<<<< HEAD
        return redirect("/login")
    return render_template("register.html", title="Регистрация", form=form)


@app.route("/login", methods=["GET", "POST"])
=======
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
>>>>>>> origin/master
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
<<<<<<< HEAD
<<<<<<< HEAD
        user = (
            db_sess.query(User_web)
            .filter(User_web.nickname == form.nickname.data)
            .first()
        )
=======
        user = db_sess.query(User).filter(User.nickname == form.nickname.data).first()
>>>>>>> origin/master
=======
        user = db_sess.query(User).filter(User.nickname == form.nickname.data).first()
>>>>>>> parent of b28b61c (the raw final version)
        db_sess.close()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
<<<<<<< HEAD
        return render_template(
            "login.html", message="Неправильный логин или пароль", form=form
        )
    return render_template("login.html", title="Авторизация", form=form)


@app.route("/logout")
=======
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
>>>>>>> origin/master
def logout():
    logout_user()
    return redirect("/")


<<<<<<< HEAD
@app.route("/test")
def test():
    if not request.script_root:
        request.root_path = url_for("index", _external=True)
    return render_template("session.html")


@app.route("/test2")
def test2():
    print("da")
    return jsonify()


@app.route("/get_session_data/<session_id>")
def get_session_data(session_id):
    if not request.script_root:
        request.root_path = url_for("index", _external=True)
    db_sess = db_session.create_session()
    session = (
        db_sess.query(GameChess)
        .filter(GameChess.id == session_id, GameChess.is_finished == 0)
        .first()
    )
    if not session:
        return jsonify(legit=False)
    colour = "white" if session.white_id == current_user.id else "black"
    enemy_id = session.black_id if colour == "white" else session.white_id
    position = eval(session.board)
    board = to_site_board(position[-1].split()[0])
    enemy = db_sess.query(User).filter(User.id == enemy_id).first().nickname
    whose_turn = "white" if position[-1].split()[1] == "w" else "black"
    db_sess.close()
    return jsonify(
        legit=True, colour=colour, board=board, whose_turn=whose_turn, enemy=enemy
    )


@app.route("/get_board/<session_id>")
def get_board(session_id):
    if not request.script_root:
        request.root_path = url_for("index", _external=True)
    db_sess = db_session.create_session()
<<<<<<< HEAD
    session = db_sess.query(Game).filter(Game.id == session_id).first()
=======
@app.route('/test')
def test():
    if not request.script_root:
        request.root_path = url_for('index', _external=True)
    return render_template('session.html')


@app.route('/test2')
def test2():
    print('da')
    return jsonify()


@app.route('/get_session_data/<session_id>')
def get_session_data(session_id):
    if not request.script_root:
        request.root_path = url_for('index', _external=True)
    db_sess = db_session.create_session()
    session = db_sess.query(GameChess).filter(GameChess.id == session_id, GameChess.is_finished == 0).first()
    if not session:
        return jsonify(legit=False)
    colour = 'white' if session.white_id == current_user.id else 'black'
    enemy_id = session.black_id if colour == 'white' else session.white_id
    position = eval(session.board)
    board = to_site_board(position[-1].split()[0])
    enemy = db_sess.query(User).filter(User.id == enemy_id).first().nickname
    whose_turn = "white" if position[-1].split()[1] == "w" else "black"
    db_sess.close()
    return jsonify(legit=True, colour=colour, board=board, whose_turn=whose_turn, enemy=enemy)


@app.route('/get_board/<session_id>')
def get_board(session_id):
    if not request.script_root:
        request.root_path = url_for('index', _external=True)
    db_sess = db_session.create_session()
    session = db_sess.query(GameChess).filter(GameChess.id == session_id).first()
>>>>>>> origin/master
=======
    session = db_sess.query(GameChess).filter(GameChess.id == session_id).first()
>>>>>>> parent of b28b61c (the raw final version)
    if not session:
        return jsonify(legit=False)
    board = to_site_board(eval(session.board)[-1].split()[0])
    db_sess.close()
    return jsonify(legit=True, board=board, end=session.is_finished == 1)


<<<<<<< HEAD
@app.route("/movement/<data>")
def movement(data):
    if not request.script_root:
        request.root_path = url_for("index", _external=True)
    session_id = data.split("&")[0]
    cord_from = (int(data.split("&")[1][0]) - 1, 8 - int(data.split("&")[1][1]))
    cord_to = (int(data.split("&")[2][0]) - 1, 8 - int(data.split("&")[2][1]))
    db_sess = db_session.create_session()
    session = (
        db_sess.query(GameChess)
        .filter(GameChess.id == session_id, GameChess.is_finished == 0)
        .first()
    )
=======
@app.route('/movement/<data>')
def movement(data):
    if not request.script_root:
        request.root_path = url_for('index', _external=True)
    session_id = data.split('&')[0]
    cord_from = (int(data.split('&')[1][0]) - 1, 8 - int(data.split('&')[1][1]))
    cord_to = (int(data.split('&')[2][0]) - 1, 8 - int(data.split('&')[2][1]))
    db_sess = db_session.create_session()
    session = db_sess.query(GameChess).filter(GameChess.id == session_id, GameChess.is_finished == 0).first()
>>>>>>> origin/master
    if not session:
        return jsonify(legit=False)
    board = eval(session.board)
    chess = Chess(board[-1])
    print(cord_from, cord_to)
    SOME_INSTANCE = chess.move(*cord_from, *cord_to)
    print(SOME_INSTANCE)
    if SOME_INSTANCE:
        fen = chess.get_fen()
        board.append(fen)
        session.board = str(board)
        db_sess.commit()
    db_sess.close()
    return jsonify(legit=SOME_INSTANCE)


<<<<<<< HEAD
@app.route("/get_statement/<data>")
=======
@app.route('/get_statement/<data>')
>>>>>>> origin/master
def get_statement(data):
    if not request.script_root:
        request.root_path = url_for("index", _external=True)
    session_id = data.split("&")[0]
    colour = data.split("&")[1]
    db_sess = db_session.create_session()
<<<<<<< HEAD
<<<<<<< HEAD
    session = db_sess.query(Game).filter(Game.id == session_id).first()
=======
    session = db_sess.query(GameChess).filter(GameChess.id == session_id).first()
>>>>>>> origin/master
=======
    session = db_sess.query(GameChess).filter(GameChess.id == session_id).first()
>>>>>>> parent of b28b61c (the raw final version)
    if not session:
        return jsonify(legit=False)
    chess = Chess(eval(session.board)[-1])
    mate = chess.mate
    stalemate = chess.stalemate
    shah = chess.shah
    draw = chess.draw
    to_who = chess.to_who
    if draw or mate or stalemate:
        session.is_finished = 1
        db_sess.commit()
    db_sess.close()
<<<<<<< HEAD
    return jsonify(
        legit=True, stalemate=stalemate, mate=mate, shah=shah, draw=draw, to_who=to_who
    )


@app.route("/get_permission/<data>")
def get_permission(data):
    if not request.script_root:
        request.root_path = url_for("index", _external=True)
    db_sess = db_session.create_session()
    if (
        db_sess.query(GameChess)
        .filter(GameChess.id == data, GameChess.is_finished == 0)
        .first()
    ):
        db_sess.close()
        print("permission:", True)
        return jsonify(permission=True)
    db_sess.close()
    print("permission:", False)
    return jsonify(permission=False)


@app.route("/get_my_sessions")
def get_my_sessions():
    if not request.script_root:
        request.root_path = url_for("index", _external=True)
    db_sess = db_session.create_session()
    if (
        db_sess.query(GameChess)
        .filter(
            (
                (GameChess.white_id == current_user.id)
                | (GameChess.black_id == current_user.id)
            ),
            GameChess.is_finished == 0,
        )
        .first()
    ):
=======
    return jsonify(legit=True, stalemate=stalemate, mate=mate, shah=shah, draw=draw, to_who=to_who)


@app.route('/get_permission/<data>')
def get_permission(data):
    if not request.script_root:
        request.root_path = url_for('index', _external=True)
    db_sess = db_session.create_session()
    if db_sess.query(GameChess).filter(GameChess.id == data, GameChess.is_finished == 0).first():
        db_sess.close()
        print('permission:', True)
        return jsonify(permission=True)
    db_sess.close()
    print('permission:', False)
    return jsonify(permission=False)


@app.route('/get_my_sessions')
def get_my_sessions():
    if not request.script_root:
        request.root_path = url_for('index', _external=True)
    db_sess = db_session.create_session()
    if db_sess.query(GameChess).filter(((GameChess.white_id == current_user.id) | (GameChess.black_id == current_user.id)), GameChess.is_finished == 0).first():
>>>>>>> origin/master
        have_sessions = True
    else:
        have_sessions = False
    db_sess.close()
<<<<<<< HEAD
    print("have_sessions:", have_sessions)
    return jsonify(have_sessions=have_sessions)


@app.route("/resign/<string:session_id>")
def resign(session_id):
    if not request.script_root:
        request.root_path = url_for("index", _external=True)
    db_sess = db_session.create_session()
    session = db_sess.query(GameChess).filter(GameChess.id == session_id).first()
    session.is_finished = 1
    db_sess.commit()
    db_sess.close()
    print("resign")
    return jsonify()


@app.route("/is_finished/<string:session_id>")
def is_finished(session_id):
    if not request.script_root:
        request.root_path = url_for("index", _external=True)
    db_sess = db_session.create_session()
<<<<<<< HEAD
    is_finished = db_sess.query(Game).filter(Game.id == session_id).first().is_finished
=======
    print('have_sessions:', have_sessions)
    return jsonify(have_sessions=have_sessions)


@app.route('/resign/<string:session_id>')
def resign(session_id):
    if not request.script_root:
        request.root_path = url_for('index', _external=True)
    db_sess = db_session.create_session()
    session = db_sess.query(GameChess).filter(GameChess.id == session_id).first()
    session.is_finished = 1
    db_sess.commit()
    db_sess.close()
    print('resign')
    return jsonify()


@app.route('/is_finished/<string:session_id>')
def is_finished(session_id):
    if not request.script_root:
        request.root_path = url_for('index', _external=True)
    db_sess = db_session.create_session()
    is_finished = db_sess.query(GameChess).filter(GameChess.id == session_id).first().is_finished
>>>>>>> origin/master
=======
    is_finished = (
        db_sess.query(GameChess).filter(GameChess.id == session_id).first().is_finished
    )
>>>>>>> parent of b28b61c (the raw final version)
    db_sess.close()
    return jsonify(is_finished=bool(is_finished))


<<<<<<< HEAD
def rotate_board(
    board: list[list],
):
=======
def main():
    db_session.global_init(PATH_TO_DB_FOLDER + "/db/data.db")
    app.run(host='0.0.0.0', port=CONFIG['port'])


def rotate_board(board: [[], ]):
>>>>>>> origin/master
    return [board[i].reverse() for i in range(7, -1, -1)]


def to_site_board(board: str):
<<<<<<< HEAD
    return (
        board.replace("1", "F")
        .replace("2", "FF")
        .replace("3", "FFF")
        .replace("4", "FFFF")
        .replace("5", "FFFFF")
        .replace("6", "FFFFFF")
        .replace("7", "FFFFFFF")
        .replace("8", "FFFFFFFF")
    )


def to_FEN_board(board: str):
    return (
        board.replace("FFFFFFFF", "8")
        .replace("FFFFFFF", "7")
        .replace("FFFFFF", "6")
        .replace("FFFFF", "5")
        .replace("FFFF", "4")
        .replace("FFF", "3")
        .replace("FF", "2")
        .replace("F", "1")
    )


db_session.global_init(join("database", "data.db"))
app.run(host="0.0.0.0", port=CONFIG["port"])
=======
    return board.replace('1', 'F').replace('2', 'FF').replace('3', 'FFF').replace('4', 'FFFF').replace('5', 'FFFFF').replace('6', 'FFFFFF').replace('7', 'FFFFFFF').replace('8', 'FFFFFFFF')


def to_FEN_board(board: str):
    return board.replace('FFFFFFFF', '8').replace('FFFFFFF', '7').replace('FFFFFF', '6').replace('FFFFF', '5').replace('FFFF', '4').replace('FFF', '3').replace('FF', '2').replace('F', '1')


if __name__ == '__main__':
    main()
else:
    main()
>>>>>>> origin/master
