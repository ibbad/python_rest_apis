
# System modules
import os


# 3rd party dependencies
import connexion
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


basedir = os.path.abspath(os.path.dirname(__file__))

# Create connexion application instance
connex_app = connexion.App(__name__, specification_dir=basedir)

# Get underlying Flask App instance
app = connex_app.app

# Build SQLite URL for SQL-Alchemy
sqlite_url = "sqlite:////" + os.path.join(basedir, "people.db")

# Configure the SqlAlchemy part of app instance
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = sqlite_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create SqlAlchemy db instance
db = SQLAlchemy(app)

# Initialize Marshmallow
ma = Marshmallow(app)
