from flask_wtf import FlaskForm
from wtforms import SubmitField


class StartGameForm(FlaskForm):
    submit = SubmitField('Начать игру')