from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Actor(db.Model):
  __tablename__ = 'Actor'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  age = db.Column(db.String)
  gender = db.Column(db.String)
  image_link = db.Column(db.String(500))
  
  movies = db.relationship('Movie', backref='actor', lazy=True)

  def to_dict(self):
    return {
      'id': self.id,
      'name': self.name,
      'age': self.age,
      'gender': self.gender,
      'image_link': self.image_link
    }

  def __repr__(self):
    return f'<<Actor {self.id} {self.name}>'

class Movie(db.Model):
  __tablename__ = 'Movie'

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String)
  release_date = db.Column(db.String(120))
  image_link = db.Column(db.String(500))
  
  actors = db.relationship('Actor', backref='movie', lazy=True)

  def to_dict(self):
    return {
      'id': self.id,
      'title': self.title,
      'release_date': self.release_date,
      'image_link': self.image_link
    }
      
  def __repr__(self):
    return f'<Movie {self.id} {self.title}>'
