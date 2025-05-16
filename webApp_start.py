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
from flask_restful import Api
from database import db_session, games_resource
from database.users_web import User_web
from database.games import Game
from webApp.forms.register import RegisterForm
from webApp.forms.login import LoginForm
from game_logic.chess_logic import Chess
from os.path import join
import sys

# for linux absolute path
# for windows relative path
ADMIN_IDs = [1]
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
api = Api(app)
api.add_resource(games_resource.GamesListResource, "/api/games")
api.add_resource(games_resource.GamesResource, "/api/games/<int:game_id>")
# IMPORTANT SECRET KEY
app.config["SECRET_KEY"] = CONFIG["SECRET_KEY"]

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    usr = db_sess.get(User_web, user_id)
    db_sess.close()
    return usr


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
@login_required
def waiting():
    if current_user.is_authenticated:
        if not request.script_root:
            request.root_path = url_for("index", _external=True)
        db_sess = db_session.create_session()
        try:
            sess = (
                db_sess.query(Game)
                .filter(
                    (
                            (Game.white_id == current_user.id)
                            | (Game.black_id == current_user.id)
                    ),
                    Game.is_finished == 0,
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
                        db_sess.query(Game)
                                .filter(Game.black_id == -1, Game.is_finished == 0)
                                .all()
                    )
                    != 0
            ):
                game = (
                    db_sess.query(Game)
                    .filter(Game.black_id == -1, Game.is_finished == 0)
                    .first()
                )
                game.black_id = current_user.id
                db_sess.commit()
                return redirect(f"/session/{game.id}")
            game = Game(white_id=current_user.id)
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
        db_sess.query(Game)
        .filter(Game.white_id == current_user.id, Game.is_finished == 0)
        .first()
    )
    if not session:
        return jsonify(legit=False)
    if session.black_id in [-2, -1]:
        return jsonify(
            legit=True, start_game=False, black_id=session.black_id, session=session.id
        )
    enemy = db_sess.get(User_web, session.black_id)
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
                    db_sess.query(Game)
                    .filter(Game.id == int(way), Game.is_finished == 0)
                    .first()
                )
                if not sess:
                    raise Exception
                if sess.black_id in (-1, -2):
                    sess.black_id = current_user.id
                    db_sess.commit()
                    db_sess.close()
                    return redirect(f"/session/{int(way)}")
                else:
                    raise Exception
            except Exception:
                db_sess.close()
                return render_template(
                    "start_game.html", message="Неправильный id игры"
                )
        elif way == "create":
            db_sess = db_session.create_session()
            obj = Game(white_id=current_user.id)
            obj.black_id = -2
            db_sess.add(obj)
            db_sess.commit()
            db_sess.close()
        return redirect(f"/waiting_for_players")
    else:
        return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template(
                "register.html",
                title="Регистрация",
                form=form,
                message="Пароли не совпадают",
            )
        db_sess = db_session.create_session()
        if (
                db_sess.query(User_web)
                        .filter(User_web.nickname == form.nickname.data)
                        .first()
        ):
            return render_template(
                "register.html",
                title="Регистрация",
                form=form,
                message="Такой пользователь уже есть",
            )
        user = User_web(nickname=form.nickname.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        db_sess.close()
        return redirect("/login")
    return render_template("register.html", title="Регистрация", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = (
            db_sess.query(User_web)
            .filter(User_web.nickname == form.nickname.data)
            .first()
        )
        db_sess.close()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template(
            "login.html", message="Неправильный логин или пароль", form=form
        )
    return render_template("login.html", title="Авторизация", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")


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
        db_sess.query(Game).filter(Game.id == session_id, Game.is_finished == 0).first()
    )
    if not session:
        return jsonify(legit=False)
    colour = "white" if session.white_id == current_user.id else "black"
    enemy_id = session.black_id if colour == "white" else session.white_id
    position = eval(session.board)
    board = to_site_board(position[-1].split()[0])
    enemy = db_sess.query(User_web).filter(User_web.id == enemy_id).first().nickname
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
    session = db_sess.query(Game).filter(Game.id == session_id).first()
    if not session:
        return jsonify(legit=False)
    board = to_site_board(eval(session.board)[-1].split()[0])
    db_sess.close()
    return jsonify(legit=True, board=board, end=session.is_finished == 1)


@app.route("/movement/<data>")
def movement(data):
    if not request.script_root:
        request.root_path = url_for("index", _external=True)
    session_id = data.split("&")[0]
    cord_from = (int(data.split("&")[1][0]) - 1, 8 - int(data.split("&")[1][1]))
    cord_to = (int(data.split("&")[2][0]) - 1, 8 - int(data.split("&")[2][1]))
    db_sess = db_session.create_session()
    session = (
        db_sess.query(Game).filter(Game.id == session_id, Game.is_finished == 0).first()
    )
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


@app.route("/get_statement/<data>")
def get_statement(data):
    if not request.script_root:
        request.root_path = url_for("index", _external=True)
    session_id = data.split("&")[0]
    colour = data.split("&")[1]
    db_sess = db_session.create_session()
    session = db_sess.query(Game).filter(Game.id == session_id).first()
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
    return jsonify(
        legit=True, stalemate=stalemate, mate=mate, shah=shah, draw=draw, to_who=to_who
    )


@app.route("/get_permission/<data>")
def get_permission(data):
    if not request.script_root:
        request.root_path = url_for("index", _external=True)
    db_sess = db_session.create_session()
    if db_sess.query(Game).filter(Game.id == data, Game.is_finished == 0).first():
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
            db_sess.query(Game)
                    .filter(
                ((Game.white_id == current_user.id) | (Game.black_id == current_user.id)),
                Game.is_finished == 0,
            )
                    .first()
    ):
        have_sessions = True
    else:
        have_sessions = False
    db_sess.close()
    print("have_sessions:", have_sessions)
    return jsonify(have_sessions=have_sessions)


@app.route("/resign/<string:session_id>")
def resign(session_id):
    if not request.script_root:
        request.root_path = url_for("index", _external=True)
    db_sess = db_session.create_session()
    session = db_sess.query(Game).filter(Game.id == session_id).first()
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
    is_finished = db_sess.query(Game).filter(Game.id == session_id).first().is_finished
    db_sess.close()
    return jsonify(is_finished=bool(is_finished))


@app.route("/adminpanel/", defaults={"command": None})
@app.route("/adminpanel/<string:command>")
def adminpanel(command):
    global ADMIN_IDs
    if current_user.is_authenticated and current_user.id in ADMIN_IDs:
        if not request.script_root:
            request.root_path = url_for("index", _external=True)
        if not command:
            return render_template('adminpanel.html')
        db_sess = db_session.create_session()
        success = True
        try:
            if command == 'deleteAllGames':
                db_sess.delete(Game)
            elif command == 'endAllGames':
                for i in db_sess.query(Game).filter(Game.is_finished == 0).all():
                    i.is_finished = 1
            elif command == 'deleteAllUsersButAdmin':
                db_sess.query(User_web).filter(User_web.id not in ADMIN_IDs).delete()
                ADMIN_IDs = [1]
            elif command.startswith('deleteUser'):
                db_sess.query(User_web).filter(User_web.id == int(command.split('&')[1])).delete()
                if int(command.split('&')[1]) in ADMIN_IDs:
                    ADMIN_IDs.remove(int(command.split('&')[1]))
            elif command.startswith('addUser'):
                user = User_web(
                    nickname=command.split('&')[1]
                )
                user.set_password(command.split('&')[2])
                db_sess.add(user)
            elif command.startswith('addAdmin'):
                ADMIN_IDs.append(int(command.split('&')[1]))
            else:
                success = False
            db_sess.commit()
        except Exception:
            print('bad')
            success = False
        db_sess.close()
        return jsonify(success=success)
    print('bad2')
    return redirect("/")


def rotate_board(
        board: list[list],
):
    return [board[i].reverse() for i in range(7, -1, -1)]


def to_site_board(board: str):
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


db_session.global_init(join(PATH_TO_DB_FOLDER, "database", "data.db"))
app.run(host="0.0.0.0", port=CONFIG["port"])
