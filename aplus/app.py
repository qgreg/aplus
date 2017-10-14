from flask import Flask


def create_app(config_filename):
    """Create and configure the Flask app, including initiating the database,
    registering the login_blueprint and cateogry blueprints, and establishes
    CSRF protection.

    Args:
        config_filename:  the configuration filename

    Returns:
        The Flask app.
    """
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)

    # Initiate the database
    from aplus.models import db
    db.init_app(app)

    # Register the login blueprint that manages user Google and Facebook logins
    from aplus.api.views import api
    app.register_blueprint(api)

    return app
