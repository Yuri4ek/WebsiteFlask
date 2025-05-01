from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, \
    IntegerField, EmailField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    nickname_email = EmailField('Никнейм или Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')
