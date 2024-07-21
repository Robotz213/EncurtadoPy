from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length

class ShortenerForm(FlaskForm):
    
    url_encurtar = StringField(label="Your URL", validators=[DataRequired()]) 
    submit = SubmitField(label="Shorten!")
