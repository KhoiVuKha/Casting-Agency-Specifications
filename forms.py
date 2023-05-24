from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, AnyOf, URL, Optional
from wtforms.validators import Regexp, ValidationError, re

def isValidAge(form, field):
    if not re.search(r'^[0-9\-\+]+$', field.data):
        raise ValidationError("Invalid age.")

class ActorForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    age = StringField(
        'age', validators=[isValidAge]
    )
    gender = SelectMultipleField(
        'gender', validators=[DataRequired()],
        choices=[
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Other', 'Other'),
        ]
    )
    image_link = StringField(
        'image_link', validators=[Optional(), URL()]
    )

class MovieForm(Form):
    title = StringField(
        'title', validators=[DataRequired()]
    )
    release_date = StringField(
        'release_date', validators=[DataRequired()]
    )
    image_link = StringField(
        'image_link', validators=[Optional(), URL()]
    )
