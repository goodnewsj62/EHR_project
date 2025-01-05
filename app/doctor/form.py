from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    DateField,
    EmailField,
    IntegerField,
    TextAreaField,
    StringField,
    SelectField,
    RadioField,
    TimeField,
)
from wtforms.validators import DataRequired, Length, Email


class PatientForm(FlaskForm):
    fullname = StringField(validators=[DataRequired(), Length(min=3, max=100)])
    email = EmailField(
        validators=[
            DataRequired(),
            Length(min=6, max=100),
            Email(),
        ]
    )

    phone = StringField(validators=[DataRequired(), Length(min=10, max=16)])
    address = StringField(validators=[DataRequired(), Length(min=3)])
    ethnicity = StringField(validators=[DataRequired(), Length(min=3)])
    age = IntegerField(validators=[DataRequired()])
    relationship_status = RadioField(
        choices=["single", "married"], validators=[DataRequired()]
    )
    allergies = TextAreaField()
    gender = SelectField(
        choices=[("male", "male"), ("female", "female")],
        validators=[DataRequired()],
    )


class PatientRecordForm(FlaskForm):
    is_immunized = BooleanField(validators=[DataRequired()])
    appointment_date = DateField(validators=[DataRequired()])
    appointment_time = TimeField(validators=[DataRequired()])
    description = TextAreaField(validators=[DataRequired(), Length(min=3)])
