from datetime import date as dt
from datetime import timedelta

from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from src.auth import login_required
from src.db import get_db

bp = Blueprint("tracker", __name__)


@bp.route("/", methods=("GET", "POST"))
@login_required
def index():
    if request.method == "POST":
        date = request.form["date"] if len(request.form["date"]) > 0 else dt.today()
        return redirect(url_for("tracker.date_logs", date=date))
    db = get_db()
    dates = db.execute(
        "SELECT DISTINCT date FROM calorie_log WHERE user_id = (?)",
        (g.user["id"],),
    ).fetchall()

    dates = [dt.fromisoformat(d["date"]) for d in dates]

    return render_template("tracker/index.html", today=dt.today(), dates=dates)


# FILTERS
@bp.app_template_filter()
def prev_day(value: dt) -> dt:
    return value - timedelta(days=1)


@bp.app_template_filter()
def next_day(value: dt) -> dt:
    return value + timedelta(days=1)


# LOGS PER DAY
@bp.route("/logs/<date>", methods=("GET",))
@login_required
def date_logs(date: str):
    db = get_db()
    logs = db.execute(
        "SELECT id, food, calories"
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


@bp.route("/log/<int:id>/delete", methods=("POST",))
@login_required
def delete(id: int):
    db = get_db()
    date = db.execute(
        "SELECT date(date) AS date FROM calorie_log WHERE id = (?)",
        (id,),
    ).fetchone()["date"]

    db.execute("DELETE FROM calorie_log WHERE id == (?)", (id,))
    db.commit()

    return redirect(url_for("tracker.date_logs", date=date))
