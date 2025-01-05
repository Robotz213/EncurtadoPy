from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ShortenerForm(FlaskForm):
    """
    ShortenerForm is a form for shortening URLs.
    Attributes:
        url_encurtar (StringField): A field for the user to input the URL they want to shorten.
                                    It is required and labeled as "Your URL".
        submit (SubmitField): A submit button labeled "Shorten!" to submit the form.
    """

    url_encurtar = StringField(label="Your URL", validators=[DataRequired()])
    submit = SubmitField(label="Shorten!")
