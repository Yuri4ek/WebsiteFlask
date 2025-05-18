from flask_wtf import FlaskForm
from wtforms import (PasswordField, StringField, TextAreaField, SubmitField,
                     EmailField, IntegerField)
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    nickname = StringField('Никнейм', validators=[DataRequired()],
                           render_kw={"placeholder": "Никнейм"})
    email = EmailField('Почта', validators=[DataRequired()],
                       render_kw={"placeholder": "Почта"})
    password = PasswordField('Пароль', validators=[DataRequired()],
                             render_kw={"placeholder": "Пароль"})
    submit = SubmitField('Создать')
