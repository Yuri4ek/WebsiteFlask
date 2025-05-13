from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email


class EditProfileForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    city = StringField('Город')
    bio = TextAreaField('О себе')
    submit = SubmitField('Сохранить изменения')
