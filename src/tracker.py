from datetime import date as dt

from flask import Blueprint, flash, g, redirect, render_template, request, url_for

# from werkzeug.exceptions import abort
from src.auth import login_required
from src.db import get_db

bp = Blueprint("tracker", __name__)


@bp.route("/")
@login_required
def index():
    db = get_db()
    dates = db.execute(
        "SELECT DISTINCT date(date) AS date FROM calorie_log WHERE user_id = (?)",
        (g.user["id"],),
    ).fetchall()

    return render_template("tracker/index.html", dates=dates)


# LOGS PER DAY


@bp.route("/logs/<date>", methods=("GET",))
@login_required
def date_logs(date: str):
    db = get_db()
    logs = db.execute(
        "SELECT date, food, calories"
        " FROM calorie_log c"
        " WHERE user_id == (?) AND date(date) == (?)"
        " ORDER BY date ASC;",
        (
            g.user["id"],
            date,
        ),
    ).fetchall()

    return render_template(
        "tracker/date_logs.html", date=dt.fromisoformat(date), logs=logs
    )


@bp.route("/logs/<date>/add", methods=("GET", "POST"))
@login_required
def create_log(date: str):
    if request.method == "POST":
        food = request.form["food"]
        calories = request.form["calories"]
        error = None

        if not food:
            error = "Food is required"
        elif not calories:
            error = "Calorie amount is required"

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO calorie_log (date, user_id, food, calories)"
                " VALUES(?, ?, ?, ?)",
                (date, g.user["id"], food, calories),
            )
            db.commit()
            return redirect(url_for("tracker.date_logs", date=date))

    return render_template("tracker/add.html", date=dt.fromisoformat(date))
