from flask import Blueprint, render_template


app = Blueprint("ehr", __name__)


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")


@app.route("/faq", methods=["GET"])
def faq():
    return render_template("faq.html")
