"""Forms for our demo Flask app."""

from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, BooleanField, SelectField
from wtforms.validators import InputRequired, Optional, URL, AnyOf, NumberRange



class AddPetForm(FlaskForm):
    """Form for adding pet."""

    name = StringField(
        "Pet Name",
        validators=[InputRequired()]
    )

    species = SelectField(
        'Species',
        choices=[('Dog', 'Dog'), ('Cat', 'Cat'), ('Porcupine', 'Porcupine')],
        validators=[InputRequired(), AnyOf(['Dog', 'Cat', 'Porcupine'])]
    )

    photo_url = StringField(
        "Photo URL", 
        validators=[Optional(), URL()]
    )

    age = IntegerField(
        "Age", 
        validators=[InputRequired(), NumberRange(0, 30)]
    )

    notes = StringField(
        "Notes", 
        validators=[Optional()]
    )     

class EditPetForm(FlaskForm):
    """Form for editing pet."""


    photo_url = StringField(
        "Photo URL", 
        validators=[Optional(), URL()]
    )

    notes = StringField(
        "Notes", 
        validators=[Optional()]
    )   

    available = BooleanField(
        "Available",
        validators=[Optional()]
    )  