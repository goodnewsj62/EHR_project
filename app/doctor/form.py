from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    DateField,
    EmailField,
    IntegerField,
    MultipleFileField,
    TextAreaField,
    StringField,
    SelectField,
    RadioField,
    TimeField,
)
from wtforms.validators import DataRequired, Length, Email
from flask_wtf.file import FileRequired, FileAllowed


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
    is_immunized = BooleanField(validators=[])
    appointment_date = DateField(validators=[DataRequired()])
    appointment_time = TimeField(validators=[DataRequired()])
    description = TextAreaField(validators=[DataRequired(), Length(min=3)])
    photos = MultipleFileField(validators=[FileAllowed(["jpg", "png"], "Images only!")])
