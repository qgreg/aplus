# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database - we are working with
SQLALCHEMY_DATABASE_URI = 'postgres://iqwfnjnbuvogsx:3e72c5889e1eb835a4bf06c8b4a1bb3e3d972dc0ded92f7a39de6bd6ba3f2a58@ec2-107-22-252-91.compute-1.amazonaws.com:5432/dc7nivdqo1av4p'  # noqa

# Turn off tracking modifications of objects and emiting signals
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for signing the data.
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"
