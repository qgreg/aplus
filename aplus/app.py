from flask import Flask
from flask_wtf.csrf import CsrfProtect

# Get ready to load CSRF protection
csrf = CsrfProtect()


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

    # Register the category blueprint that manages category and item CRUD
    #from itemcatalog.category.views import category
    #app.register_blueprint(category)

    # Establish CSRF protection but exempt the login blueprint
    csrf.init_app(app)
    # csrf.exempt(login_blueprint)

    return app
