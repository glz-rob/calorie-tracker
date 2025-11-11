from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from src.auth import login_required
from src.db import get_db

bp = Blueprint("tracker", __name__)


@bp.route("/")
@login_required
def index():
    db = get_db()
    logs = db.execute(
        "SELECT datetime, c.id, food, calories "
        "FROM calorie_log c "
        "JOIN date_log d ON c.date_id = d.id "
        "JOIN user u ON d.user_id = u.id "
        "WHERE u.id == (?) "
        "ORDER BY datetime ASC ",
        (g.user["id"],),
    ).fetchall()

    return render_template("tracker/index.html", logs=logs)
