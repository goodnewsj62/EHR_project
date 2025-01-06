import os
from flask import Blueprint, current_app, redirect, render_template, send_file, url_for
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


@app.route("/display_image/<filename>")
def display_image(filename):
    """
    Displays an image from the specified path.

    Args:
        filename: The name of the image file.

    Returns:
        The image file as a response.
    """
    try:
        return send_file(
            os.path.join(current_app.config["MEDIA_PATH"], "images", filename)
        )
    except FileNotFoundError:
        return "Image not found", 404
