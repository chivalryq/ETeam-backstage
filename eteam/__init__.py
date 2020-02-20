from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, configure_uploads
import click
import logging
app = Flask(__name__)
app.config.from_pyfile('settings.py')
db=SQLAlchemy(app)
photos = UploadSet('PHOTO')
configure_uploads(app, photos)
from .views.user import user_mod
from .views.team import team_mod
from .views.person import person_mod

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/url')
def url():
    return str(app.url_map)




app.register_blueprint(user_mod)
app.register_blueprint(team_mod)
app.register_blueprint(person_mod)

@app.cli.command()
def initdb():
    # TODO 开发环境删掉drop
    db.drop_all()
    db.create_all()
    print("Drop and Initializing database")
