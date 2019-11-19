from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import click
app = Flask(__name__)
app.config.from_pyfile('settings.py')
db=SQLAlchemy(app)
from .views.user import user

@app.route('/')
def hello_world():
    return 'Hello World!'

app.register_blueprint(user)
@app.cli.command('initdb')
def initdb():
    db.create_all()
    print("Intialized database")
