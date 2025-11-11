import sqlite3
from datetime import datetime
from sqlite3 import Connection
from typing import IO, Any, cast

import click
from flask import current_app, g, Flask


def get_db() -> Connection:
    """
    If `db` is not in `g`, it creates the connection. Otherwise, it just returns `db` from `g`.
    """
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],  # type: ignore
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e: BaseException | None = None):
    """
    Removes the `db` from `g`, and then closes the connection.
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    """
    Runs the `schema.sql` script.
    """
    db = get_db()

    with cast(IO[Any], current_app.open_resource("schema.sql")) as f:
        db.executescript(f.read().decode("utf8"))


@click.command("init-db")
def init_db_command():
    """
    Clear the existing data and create new tables.
    """
    init_db()
    click.echo("Initialized the database.")


sqlite3.register_converter("timestamp", lambda v: datetime.fromisoformat(v.decode()))


def init_app(app: Flask):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
