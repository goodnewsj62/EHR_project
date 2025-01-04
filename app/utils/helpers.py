from flask import current_app, request, url_for
from flask_mail import Message
import jwt

from app import mail
from app.utils.constants import EMAIL_TEMPLATE


def account_activation_task(email, fullname):
    # try:
    encoded_jwt = jwt.encode(
        {"email": email}, current_app.config.get("SECRET_KEY"), algorithm="HS256"
    )
    url = request.url_root[:-1] + url_for("auth.verify_mail") + f"?token={encoded_jwt}"
    msg = Message(
        "Hello from Flask",
        recipients=[email],  # List of recipients
        html=EMAIL_TEMPLATE(url, fullname),
    )
    mail.send(msg)
    return True, "Email sent successfully!"


# except Exception as e:
# print("==================================", e)
# return False, f"Failed to send email"
