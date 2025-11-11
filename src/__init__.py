import os
from typing import Any, Mapping

from flask import Flask


def create_app(test_config: Mapping[str, Any] | None = None) -> Flask:
    """
    Create and configure the app
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "calorie-tracker.sqlite"),
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/hello")
    def hello():  # type: ignore
        return "Hello, World!"

    from . import auth, db, tracker

    db.init_app(app)

    app.register_blueprint(auth.bp)

    app.register_blueprint(tracker.bp)
    app.add_url_rule("/", endpoint="index")

    return app
