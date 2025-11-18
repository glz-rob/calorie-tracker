from datetime import date as dt
from datetime import timedelta

from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from src.auth import login_required
from src.db import get_db

bp = Blueprint("tracker", __name__)


@bp.route("/", methods=("GET",))
@bp.route("/<year>/<month>", methods=("GET",))
@login_required
def index(year: str | None = None, month: str | None = None):
    year = str(dt.today().year) if year is None else year
    month = dt.today().strftime("%m") if month is None else month

    db = get_db()
    dates = db.execute(
        "SELECT DISTINCT date "
        "FROM calorie_log "
        "WHERE user_id = (?) "
        "   AND strftime('%m', date) = (?) "
        "   AND strftime('%Y', date) = (?) "
        "ORDER BY date",
        (g.user["id"], month, year),
    ).fetchall()

    dates = [dt.fromisoformat(d["date"]) for d in dates]

    return render_template("tracker/index.html", dates=dates)


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
        "SELECT id, amount, food, calories"
        " FROM calorie_log c"
        " WHERE user_id == (?) AND date(date) == (?)"
        " ORDER BY date ASC;",
        (
            g.user["id"],
            date,
        ),
    ).fetchall()
    total_calories = sum([int(x["calories"]) for x in logs])

    return render_template(
        "tracker/date_logs.html",
        date=dt.fromisoformat(date),
        logs=logs,
        total_calories=total_calories,
    )


@bp.route("/logs/<date>/add", methods=("GET", "POST"))
@login_required
def create_log(date: str):
    if request.method == "POST":
        food = request.form["food"]
        calories = request.form["calories"]
        amount = request.form["amount"]
        error = None

        if not amount:
            error = "Amount is required"
        elif int(amount) <= 0:
            error = "Amount must be more than 0"
        elif not food or len(food.strip()) <= 0:
            error = "Food is required"
        elif not calories:
            error = "Calories are required"
        elif int(calories) <= 0:
            error = "Calories amount must more than 0"

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO calorie_log (date, user_id, food, amount, calories)"
                " VALUES(?, ?, ?, ?, ?)",
                (date, g.user["id"], food, amount, calories),
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
