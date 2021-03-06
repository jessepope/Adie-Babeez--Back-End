from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_DATABASE_URI")
    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_TEST_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_TEST_DATABASE_URI")

    from app.models.user import User
    from app.models.post import Post
    from app.models.comment import Comment
    

    # Setup DB
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints here
    from .routes_user import user_bp
    app.register_blueprint(user_bp)
    from .routes_post import post_bp
    app.register_blueprint(post_bp)
    from .routes_comment import comment_bp
    app.register_blueprint(comment_bp)


    CORS(app)
    return app
