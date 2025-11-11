from flask import Blueprint, render_template  # , request, url_for, flash, g, redirect
# from werkzeug.exceptions import abort

bp = Blueprint("tracker", __name__)


@bp.route("/")
def index():
    return render_template("tracker/index.html")
