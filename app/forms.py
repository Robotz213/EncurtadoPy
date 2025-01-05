from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ShortenerForm(FlaskForm):

    url_encurtar = StringField(label="Your URL", validators=[DataRequired()])
    submit = SubmitField(label="Shorten!")
