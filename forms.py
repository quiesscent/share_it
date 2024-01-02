from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length


class Image(FlaskForm):
    image = FileField('', validators=[DataRequired(), FileAllowed(['png', 'jpg'])])



