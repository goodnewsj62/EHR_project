from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user


app = Blueprint("ehr", __name__)


@app.route("/", methods=["GET"])
def home():
    if current_user.is_authenticated:
        return redirect(url_for("doctor.dashboard"))
    return render_template("index.html")


@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")


@app.route("/faq", methods=["GET"])
def faq():
    return render_template("faq.html")
