from flask import Flask
from flask_bootstrap import Bootstrap

from app import db
from app.models import User, Post


def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    return app


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}
