"""Forms for Cupcake app."""

from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField
from wtforms.validators import InputRequired, Optional, URL
from wtforms.validators import ValidationError


class AddCupcake(FlaskForm):
    """Form for adding cupcakes."""

    flavor = StringField("Flavor", validators=[InputRequired()])
    size = StringField("Size", validators=[InputRequired()])
    rating = StringField("Rating", validators=[InputRequired()])
    image = StringField("Image", validators=[InputRequired()])
