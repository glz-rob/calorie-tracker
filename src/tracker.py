from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from src.auth import login_required
from src.db import get_db

bp = Blueprint("tracker", __name__)


@bp.route("/")
@login_required
def index():
    db = get_db()
    dates = db.execute(
        "SELECT d.id, datetime "
        "FROM date_log d "
        "JOIN user u ON d.user_id = u.id "
        "WHERE u.id == (?) "
        "ORDER BY datetime ASC ",
        (g.user["id"],),
    ).fetchall()

    return render_template("tracker/index.html", dates=dates)


@bp.route("/logs/<int:date_id>", methods=("GET",))
def date_logs(date_id: int):
    db = get_db()
    date = db.execute(
        "SELECT datetime FROM date_log WHERE id == (?)", (date_id,)
    ).fetchone()
    logs = db.execute(
        "SELECT food, calories "
        "FROM calorie_log c "
        "JOIN date_log d ON c.date_id = d.id "
        "JOIN user u ON d.user_id = u.id "
        "WHERE u.id == (?) AND d.id == (?) "
        "ORDER BY datetime ASC;",
        (
            g.user["id"],
            date_id,
        ),
    ).fetchall()

    return render_template("tracker/date_logs.html", date=date, logs=logs)
