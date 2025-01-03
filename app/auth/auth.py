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

        if not user.email_verified:
            flash("please verify your account to activate", category="error")
            return render_template("auth/login.html", form=form)

        if user and valid_password:
            login_user(user, remember=True)
            flash("login successful", category="success")
            next_page = request.args.get("next")
            if next_page and safe_url(next_page):
                return redirect(next_page or url_for("ehr.home"))
            return redirect(url_for("ehr.home"))

        else:
            flash("invalid login credentials", category="error")

    return render_template("auth/login.html", form=form)


@auth.route("/signup", methods=["POST", "GET"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        password = generate_password_hash(form.password.data)
        user = User(
            email=form.email.data,
            password=password,
        )

        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        flash("signup successful", category="success")
        next_page = request.args.get("next")
        if next_page:
            return redirect(url_for("auth.login") + f"?next={next_page}")
        return redirect(url_for("auth.login"))
    return render_template("auth/signup.html", form=form)


@auth.route("/verify-email", methods=["POST", "GET"])
def verify_mail(token):
    if request.method == "post":
        secret = current_app.config.get("SECRET_KEY")
        try:
            decoded_jwt = jwt.decode(token, secret, algorithms=["HS256"])
            user = User.query.filter_by(email=decoded_jwt.get("email")).first()
            if user:
                user.email_verified = True
            db.session.commit()
            flash("email verification succedded", category="success")
        except Exception as e:
            flash("email vedrification failed", category="error")
            # log excpetion
            pass

    return render_template()


@auth.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return redirect(url_for("erh.home"))
