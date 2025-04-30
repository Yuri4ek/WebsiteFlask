from flask_wtf import FlaskForm
from wtforms import (PasswordField, StringField, TextAreaField, SubmitField,
                     EmailField, IntegerField)
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    surname = StringField('Фамилия пользователя', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    age = IntegerField('Возраст пользователя', validators=[DataRequired()])
    position = StringField('Сфера деятельности', validators=[DataRequired()])
    speciality = StringField('Специальность', validators=[DataRequired()])
    address = EmailField('Адрес', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль',
                                   validators=[DataRequired()])
    submit = SubmitField('Войти')