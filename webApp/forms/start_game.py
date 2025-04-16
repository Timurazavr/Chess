import wtforms
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField


class StartGameForm(FlaskForm):
    submit = SubmitField('Начать игру')


class WaitingForm(FlaskForm):
    submit = SubmitField('Обнови, может кто нибудь нашелся')
