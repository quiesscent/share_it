from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired


class Image(FlaskForm):
    image = FileField('', validators=[DataRequired(), FileAllowed(['png', 'jpg'])])



