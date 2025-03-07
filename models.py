import os
from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from sqlalchemy_utils import database_exists, create_database
import json

database_path = os.environ["DATABASE_URL"]
if database_path.startswith("postgres://"):
    database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""


def setup_db(app, database_path=database_path):
    if not database_exists(database_path):
        create_database(database_path)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    db.create_all()


class Actor(db.Model):
    __tablename__ = "Actor"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.String)
    gender = db.Column(db.String)
    image_link = db.Column(db.String(500))

    # movies = db.relationship('Movie', backref='actor', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "image_link": self.image_link,
        }

    """
  insert()
    inserts a new model into a database
    the model must have a unique name
    the model must have a unique id or null id
  """

    def insert(self):
        db.session.add(self)
        db.session.commit()

    """
  delete()
    deletes a new model into a database
    the model must exist in the database
  """

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    """
  update()
    updates a new model into a database
    the model must exist in the database
  """

    def update(self):
        db.session.commit()

    def __repr__(self):
        return f"<<Actor {self.id} {self.name}>"


class Movie(db.Model):
    __tablename__ = "Movie"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.String(120))
    image_link = db.Column(db.String(500))

    # actors = db.relationship('Actor', backref='movie', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "image_link": self.image_link,
        }

    """
  insert()
    inserts a new model into a database
    the model must have a unique name
    the model must have a unique id or null id
  """

    def insert(self):
        db.session.add(self)
        db.session.commit()

    """
  delete()
    deletes a new model into a database
    the model must exist in the database
  """

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    """
  update()
    updates a new model into a database
    the model must exist in the database
  """

    def update(self):
        db.session.commit()

    def __repr__(self):
        return f"<Movie {self.id} {self.title}>"
