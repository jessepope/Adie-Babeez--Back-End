from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__)
    # app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False **we need to find out what this is and if we need it

    if test_config is None:
        app.config["INSERT DATABASE URI"] = os.environ.get(
            "INSERT DATABASE URI")
    else:
        app.config["TESTING"] = True
        app.config[" INSERT DATABASE URI"] = os.environ.get(
            "ISERT TEXT DATABASE URI")

    from app.models.user import User
    from app.models.post import Post

    db.init_app(app)
    migrate.init_app(app, db)

    # from routesfile import route bp name
    # app.register_blueprint(route bp name)



    return app
