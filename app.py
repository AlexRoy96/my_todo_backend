from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_heroku import Heroku
from environs import Env
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import psycopg2

from _config import *

app = Flask(__name__)
CORS(app)
heroku = Heroku(app)

DATABASE_URL = _config.DATABASE_URL

CONN = PSYCOPG2.CONNECT(DATABASE_URL, sslmode="require")

basedir = os.path.abspath(os.path.dirname(__file))
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Todo(db.Model):
    __tablename = "todos"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    done = db.Column(db.Boolean)

    def __init__(self, title, done):
        self.title = title
        self.done = done


class TodoSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "done")


todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)


if __name__ == "__main__":
    app.debug = True
    app.run()