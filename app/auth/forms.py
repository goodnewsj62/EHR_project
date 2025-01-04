from flask import current_app
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField
from wtforms.validators import DataRequired, Length, Email, EqualTo

from app.auth.resuable_validators import ValidateEmail, ValidatePassword


class LoginForm(FlaskForm):
    email = EmailField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])


class SignUpForm(FlaskForm):
    fullname = StringField(validators=[DataRequired(), Length(min=3, max=100)])
    email = EmailField(
        validators=[
            DataRequired(),
            Length(min=6, max=100),
            Email(
                check_deliverability=(
                    True if not current_app.config.get("DEBUG") else False
                )
            ),
            ValidateEmail(),
        ]
    )

    password = PasswordField(
        validators=[DataRequired(), Length(min=7), ValidatePassword()]
    )

    comfirm_password = PasswordField(
        label="comfirm password",
        validators=[DataRequired(), EqualTo("password", "password mismatch")],
    )


class PasswordChangeForm(FlaskForm):
    old_password = PasswordField(
        validators=[DataRequired(), Length(min=7), ValidatePassword().check_password]
    )

    new_password = PasswordField(
        validators=[DataRequired(), Length(min=7), ValidatePassword()]
    )
    comfim_password = PasswordField(
        validators=[EqualTo(new_password, "password mismatch")]
    )
