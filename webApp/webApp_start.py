from flask import Flask, request, redirect
from flask import render_template
from data import db_session
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from data.users import User
from data.onlines import Online
from data.games import GameKN
from forms.register import RegisterForm
from forms.login import LoginForm
from forms.start_game import StartGameForm, WaitingForm
from flask_htmx import HTMX, make_response

# for linux absolute path
# for windows relative path
PATH_TO_DB_FOLDER = '/home/pashok/PycharmProjects/chess/db'
app = Flask(__name__)
htmx = HTMX(app)
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


@app.route('/waiting_for_players', methods=['GET', 'POST'])
@login_required
def waiting():
    # visits_count = int(request.cookies.get("dots", 0))
    # if visits_count:

    # db_sess = db_session.create_session()
    # if not db_sess.query(Online).filter(Online.id == current_user.id).first():
    #     online = Online(
    #         id=db_sess.query(User).filter(User.id == current_user.id).first().id,
    #     )
    #     db_sess.add(online)
    #     db_sess.commit()
    # print(len(db_sess.query(Online).all()))
    # SOME_INSTANSE = False  # todo
    # form = WaitingForm()
    # if form.validate_on_submit() and SOME_INSTANSE:
    #     return redirect('/session/<id>')
    return render_template('waiting.html')


# @app.route("/cookie_test")
# def cookie_test():
#     visits_count = int(request.cookies.get("visits_count", 0))
#     if visits_count:
#         res = make_response(
#             f"Вы пришли на эту страницу {visits_count + 1} раз")
#         res.set_cookie("visits_count", str(visits_count + 1),
#                        max_age=60 * 60 * 24 * 365 * 2)
#     else:
#         res = make_response(
#             "Вы пришли на эту страницу в первый раз за последние 2 года")
#         res.set_cookie("visits_count", '1',
#                        max_age=60 * 60 * 24 * 365 * 2)
#     return res


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


if __name__ == '__main__':
    main()
else:
    main()
