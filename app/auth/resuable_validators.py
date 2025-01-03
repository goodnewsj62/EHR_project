__author__ = "goodnews john osonwa"

from typing import Any
import re
import string
from urllib import parse

from flask_login import current_user
from flask import current_app, request
from wtforms.validators import ValidationError
from werkzeug.security import check_password_hash, generate_password_hash


from app.models import User


class ValidatePassword:
    def __init__(self) -> None:
        pass

    def check_password(self, field):
        if not check_password_hash(current_user.password, field.data):
            raise ValidationError("invalid old password")

    def __call__(self, form, field) -> Any:
        if field.data == "password" and re.search(r"^\D\D+\D$", field.data):
            raise ValidationError(
                "password too common or not strong trying mixing letters numbers and capital letters"
            )

        unwanted_characters = re.sub(r"[!#@$&]", "", string.punctuation)
        unwanted_ = re.compile(r"[" + re.escape(unwanted_characters) + r"]")
        if re.search("\s", field.data) or re.search(unwanted_, field.data):
            raise ValidationError(
                f"please dont use spaces in password or these characters ({unwanted_characters})"
            )

        if not re.match(r"(?=.*\d)(?=.*[a-z])(?=.*[A-Z])", field.data):
            raise ValidationError("mix capital letters and numbers eg:ExaMp32le")
        return


class ValidateEmail:
    def __init__(self) -> None:
        pass

    def __call__(self, form, field) -> Any:
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError("user with email already exist")
        return


def safe_url(url):
    host_url = request.headers.get("host_url")
    url_parts = parse.urlsplit(url)
    host_url_parts = parse.urlsplit(host_url)

    if url_parts.netloc == "" or host_url_parts.netloc == url_parts.netloc:
        return url
    else:
        return None
