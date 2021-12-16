from flask import url_for
from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms.fields import (
    SubmitField,
    IntegerField,
    DateField,
    StringField,
    HiddenField
)
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, EqualTo, InputRequired, Length
from wtforms.widgets import TextArea
import datetime

from app.models import User

def IsInFuture(form, field):
    if datetime.datetime(field.data.year, field.data.month, field.data.day) < datetime.datetime.now():
        raise ValidationError('Kan geen spel starten in het verleden.')

class CreateGameForm(FlaskForm):
    name = StringField('Spelnaam', [InputRequired(), Length(max=32, min=4)])
    player_amount = IntegerField('Aantal spelers', [InputRequired()])
    start_date = DateField('Start datum', [InputRequired(), IsInFuture], format="%d-%m-%Y")
    submit = SubmitField('Maak aan')

class InvitePlayersForm(FlaskForm):
    email = EmailField('Emailadres', [InputRequired(), Email()])
    submit = SubmitField('Verstuur uitnodiging')

class NewMessageForm(FlaskForm):
    reply_to = HiddenField()
    text = StringField('', [InputRequired(), Length(max=500)], widget=TextArea())
    submit = SubmitField('Verstuur bericht')
