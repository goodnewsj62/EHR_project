from flask import (
    Blueprint,
    current_app,
    request,
    redirect,
    url_for,
    session,
    render_template,
    flash,
    abort,
)

from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
import jwt

from app.auth.forms import LoginForm, SignUpForm
from app.auth.resuable_validators import safe_url
from app.models import User
from app import db, login_manager
from app.utils.helpers import account_activation_task


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        identifier = form.email.data
        user = User.query.filter(User.email == identifier).first()

        valid_password = (
            check_password_hash(user.password, form.password.data) if user else False
        )

        if user and not user.email_verified:
            flash("please verify your account to activate", category="danger")
            return render_template("auth/login.html", form=form)

        if user and valid_password:
            login_user(user, remember=True)
            flash("login successful", category="success")
            next_page = request.args.get("next")
            if next_page and safe_url(next_page):
                return redirect(next_page or url_for("doctor.dashboard"))
            return redirect(url_for("doctor.dashboard"))

        else:
            flash("invalid login credentials", category="danger")

    return render_template("auth/login.html", form=form)


@auth.route("/register", methods=["POST", "GET"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        password = generate_password_hash(form.password.data)
        user = User(
            fullname=form.fullname.data,
            email=form.email.data,
            password=password,
        )

        status, resp = account_activation_task(email=user.email, fullname=user.fullname)
        if status:
            db.session.add(user)
            db.session.commit()
            flash("signup successful", category="success")
            return redirect(url_for("auth.verify_mail"))
        else:
            flash(resp, category="success")

    return render_template("auth/signup.html", form=form)


@auth.route("/verify-email", methods=["GET"])
def verify_mail():
    secret = current_app.config.get("SECRET_KEY")
    token = request.values.get("token", "")

    if token:
        print(token, request.method, secret)
        try:
            decoded_jwt = jwt.decode(token, secret, algorithms=["HS256"])
            user = User.query.filter_by(email=decoded_jwt.get("email")).first()
            if user:
                user.email_verified = True
            db.session.commit()
            flash("email verification succedded", category="success")
            return redirect(url_for("auth.login"))
        except Exception as e:
            flash("email verification failed", category="danger")
            # log excpetion
            pass

    return render_template("auth/verify-email.html")


@auth.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return redirect(url_for("ehr.home"))
