from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, \
    IntegerField, EmailField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    nickname_email = EmailField('Никнейм или Почта', validators=[DataRequired()],
                                render_kw={"placeholder": "Никнейм или Почта"})
    password = PasswordField('Пароль', validators=[DataRequired()],
                             render_kw={"placeholder": "Пароль"})
    submit = SubmitField('Войти')
