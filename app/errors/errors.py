from flask import render_template


def error_404(e):
    """
    - Displays the 404 error page.
    """
    return render_template("404.html"), 404


def error_500(e):
    """
    - Displays the 500 error page.
    """
    return render_template("500.html"), 500


def error_403(e):
    """
    - Displays the 404 error page.
    """
    return render_template("403.html"), 403
