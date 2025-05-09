from flask import Flask, request, redirect, jsonify, make_response, url_for
from flask import render_template
from data import db_session
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from data.users import User
from data.games_chess import GameChess
from forms.register import RegisterForm
from forms.login import LoginForm

# for linux absolute path
# for windows relative path
PATH_TO_DB_FOLDER = '/home/pashok/PycharmProjects/chess/db'
app = Flask(__name__)
# IMPORTANT SECRET KEY
app.config['SECRET_KEY'] = open('static/SECRET_KEY', 'r').read().strip()

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    usr = db_sess.query(User).get(user_id)
    db_sess.close()
    return usr


@app.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        if not request.script_root:
            request.root_path = url_for('index', _external=True)
        return render_template('start_game.html')
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
            sess = db_sess.query(GameChess).filter((GameChess.white_id == current_user.id) | (GameChess.black_id == current_user.id)).first()
            print(sess)
            if not sess:
                print('bad', current_user.id)
                raise Exception
            if sess.black_id == -2:
                return render_template('waiting.html')
            elif sess.black_id == -1:
                pass
            else:
                return redirect(f'/session/{sess.id}')
        except Exception as e:
            print(len(db_sess.query(GameChess).filter(GameChess.black_id == -1).all()))
            if len(db_sess.query(GameChess).filter(GameChess.black_id == -1).all()) != 0:
                game = db_sess.query(GameChess).first()
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
    session = db_sess.query(GameChess).filter(GameChess.white_id == current_user.id).first()
    if session.black_id in [-1, -2]:
        return jsonify(start_game=False, black_id=session.black_id, session=session.id)
    enemy = db_sess.query(User).filter(User.id == session.black_id).first()
    db_sess.close()
    return jsonify(start_game=True, session=session.id, enemy=enemy.nickname)


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
        print('once')
        if not request.script_root:
            request.root_path = url_for('index', _external=True)
        if way == 'random':
            return redirect('/waiting_for_players')
        elif way.isnumeric():
            db_sess = db_session.create_session()
            try:
                sess = db_sess.query(GameChess).filter(GameChess.id == int(way)).first()
                if not sess:
                    raise Exception
                if sess.black_id == -2:
                    sess.black_id = current_user.id
                    db_sess.commit()
                    db_sess.close()
                    return redirect(f'/session/{int(way)}')
                else:
                    raise Exception
            except Exception:
                db_sess.close()
                return render_template('start_game.html', message='Неправильный id игры')
        elif way == 'create':
            db_sess = db_session.create_session()
            obj = GameChess(white_id=current_user.id)
            obj.black_id = -2
            db_sess.add(obj)
            db_sess.commit()
            db_sess.close()
        return redirect(f'/waiting_for_players')
    else:
        return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form, message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.nickname == form.nickname.data).first():
            return render_template('register.html', title='Регистрация', form=form, message="Такой пользователь уже есть")
        user = User(nickname=form.nickname.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        db_sess.close()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.nickname == form.nickname.data).first()
        db_sess.close()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
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
def get_session_data(session_id):
    if not request.script_root:
        request.root_path = url_for('index', _external=True)
    db_sess = db_session.create_session()
    session = db_sess.query(GameChess).filter(
        GameChess.id == session_id).first()
    colour = 'white' if session.white_id == current_user.id else 'black'
    enemy_id = session.black_id if colour == 'white' else session.white_id
    position = eval(session.board)
    board = position[-1].split()[0]
    enemy = db_sess.query(User).filter(User.id == enemy_id).first().nickname
    whose_turn = 'white' if position[-1].split()[1] == 'w' else 'black'
    db_sess.close()
    return jsonify(colour=colour, board=board, whose_turn=whose_turn, enemy=enemy)


@app.route('/get_board/<session_id>')
def get_board(session_id):
    if not request.script_root:
        request.root_path = url_for('index', _external=True)
    db_sess = db_session.create_session()
    board = eval(db_sess.query(GameChess).filter(GameChess.id == session_id).first().board)[-1].split()[0]
    mate = False
    stalemate = False
    shah = False
    draw = False
    to_who = 'white'  # Если был шах или мат, то это поле - цвет того кому поставили шах/мат ('white' / 'black'). Если не шах/мат, то вообще безразницы чему равно
    db_sess.close()
    return jsonify(board=board, mate=mate, stalemate=stalemate, shah=shah, draw=draw, to_who=to_who)


@app.route('/movement/<data>')
def movement(data):
    if not request.script_root:
        request.root_path = url_for('index', _external=True)
    session_id = data.split('&')[0]
    cord_from = [int(i) - 1 for i in data.split('&')[1]]
    cord_to = [int(i) - 1 for i in data.split('&')[2]]
    SOME_INSTANCE = True  # todo проверка валидности хода, если валиден то сделать ход в д, ДОСКА МЕНЯЕТСЯ В КЛАССЕ ЛОГИКИ
    return jsonify(legit=SOME_INSTANCE)


@app.route('/get_statement/<data>')
def get_statement(data):
    if not request.script_root:
        request.root_path = url_for('index', _external=True)
    session_id = data.split('&')[0]
    colour = data.split('&')[1]
    mate = False
    stalemate = False
    shah = False
    draw = False
    return jsonify(legit=True, stalemate=stalemate, mate=mate, shah=shah, draw=draw)


@app.route('/get_permission/<data>')
def get_permission(data):
    if not request.script_root:
        request.root_path = url_for('index', _external=True)
    db_sess = db_session.create_session()
    if db_sess.query(GameChess).filter(GameChess.id == data).first():
        db_sess.close()
        return jsonify(permission=True)
    db_sess.close()
    return jsonify(legit=False)


@app.route('/get_my_sessions')
def get_my_sessions():
    if not request.script_root:
        request.root_path = url_for('index', _external=True)
    db_sess = db_session.create_session()
    if db_sess.query(GameChess).filter((GameChess.white_id == current_user.id) | (GameChess.black_id == current_user.id)).first():
        have_sessions = True
    else:
        have_sessions = False
    db_sess.close()
    return jsonify(have_sessions=have_sessions)


def main():
    db_session.global_init(PATH_TO_DB_FOLDER + "/data.db")
    app.run(host='0.0.0.0', port=5000)


def rotate_board(board: [[], ]):
    return [board[i].reverse() for i in range(7, -1, -1)]


if __name__ == '__main__':
    main()
else:
    main()
