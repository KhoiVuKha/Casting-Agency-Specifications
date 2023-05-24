#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify, abort
from flask_moment import Moment
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
import collections
import collections.abc
collections.Callable = collections.abc.Callable
import sys
from operator import itemgetter # for sorting lists of tuples

# import database's models
from models import db, Actor, Movie

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime
     
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')

#  Actors
#  ----------------------------------------------------------------

@app.route('/actors')
def actors():
  # Data to save all actors
  data = []
  actors = Actor.query.all()

  print(data)
  return render_template('pages/actors.html', areas=data)

@app.route('/actors/search', methods=['POST'])
def search_actors():
  search_term = request.form.get('search_term', '').strip()
  results = Actor.query.filter(Actor.name.ilike('%{}%'.format(search_term))).all()

  actor_list = []
  for actor in results:
     actor_list.append({
        "id": actor.id,
        "name": actor.name,
        "num_movies": None
        })
     
  response = {
    "count": len(results),
    "data": actor_list
  }
  print(response)
  # @todo
  return render_template('pages/search_actors.html', results=response, search_term=request.form.get('search_term', ''))

# shows the actor page with the given actor_id
@app.route('/actors/<int:actor_id>')
def show_actor(actor_id):
  actor = Actor.query.get(actor_id)
  data = actor.to_dict()

  movies = list(Actor.movies)
  movie_count = len(movies)
  data["movie_count"] = movie_count

  print(data)
  #@todo: refactor the page
  return render_template('pages/show_actor.html', actor=data)

#  Create Actor
#  ----------------------------------------------------------------

@app.route('/actors/create', methods=['GET'])
def create_actor_form():
  #@todo: refactor
  form = ActorForm()
  return render_template('forms/new_actor.html', form=form)

@app.route('/actors/create', methods=['POST'])
def create_actor_submission():
  form = ActorForm(request.form, meta={'csrf': False})
  if not form.validate():
    message = []
    for field, err in form.errors.items():
      message.append(field + ' - ' + '|'.join(err))
    flash('Errors ' + str(message))
    return redirect(url_for('create_actor_submission'))
  else:
    try:
      actor = Actor()
      actor.name = form.name.data
      actor.city = form.city.data
      actor.gender = form.gender.data
      actor.image_link = form.image_link.data

      db.session.add(actor)
      db.session.commit()
      flash('Actor: {0} created successfully!'.format(actor.name))

    except Exception as err:
      db.session.rollback()
      flash('An error occurred creating the Actor: {0}. Error: {1}'.format(actor.name, err))
      print(sys.exc_info())
    finally:
      db.session.close()
    return render_template('pages/home.html')

@app.route('/actors/<actor_id>', methods=['DELETE'])
def delete_actor(actor_id):
  try:
    actor = Actor.query.get(actor_id)
    actor_name = actor.name
    db.session.delete(actor)
    db.session.commit()
    flash('Successfully removed actor {0}.'.format(actor_name))
  except Exception as err:
    db.session.rollback()
    flash('An error occurred removing the Actor: {0}. Error: {1}'.format(actor_name, err))
  finally:
    db.session.close()
  return jsonify({'success': True})

#  Movies
#  ----------------------------------------------------------------
@app.route('/movies')
def movies():
  data = Movie.query.all()
  return render_template('pages/movies.html', movies=data)

@app.route('/movies/search', methods=['POST'])
def search_movies():
  search_term = request.form.get('search_term', '').strip()
  results = Movie.query.filter(Movie.title.ilike('%{}%'.format(search_term))).all()

  movie_list = []
  for movie in results:
    movie_list.append({
      "id": movie.id,
      "title": movie.title,
      "release_date": movie.release_date,
      "actors": None #@todo
    })

  response = {
    "count": len(movie_list),
    "data": movie_list
  }
  return render_template('pages/search_movies.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/movies/<int:movie_id>')
def show_movie(movie_id):
  movie = Movie.query.get(movie_id)
  data = movie.to_dict()

  return render_template('pages/show_movie.html', movie=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/movies/<int:movie_id>/edit', methods=['GET'])
def edit_movie(movie_id):
  form = MovieForm(request.form)
  movie = Movie.query.get(movie_id)
  movie = movie.to_dict()
  form = MovieForm(formdata=None, data=movie)
  return render_template('forms/edit_movie.html', form=form, movie=movie)

@app.route('/movies/<int:movie_id>/edit', methods=['POST'])
def edit_movie_submission(movie_id):
  movie = Movie.query.get(movie_id)
  form = MovieForm(request.form, meta={'csrf': False})
  if not form.validate():
    message = []
    for field, err in form.errors.items():
      message.append(field + ' - ' + '|'.join(err))
    flash('Errors ' + str(message))
    return redirect(url_for('edit_movie_submission', movie_id=movie_id))
  else:
    try:
      movie.title = form.title.data
      movie.release_date = form.release_date.data
      movie.image_link = form.image_link.data
      db.session.commit()
      flash('Movie: {0} updated successfully'.format(movie.title))
    except Exception as err:
      db.session.rollback()
      print(sys.exc_info())
      flash('An error occurred updating the Movie: {0}. Error: {1}'.format(movie.title, err))
    finally:
      db.session.close()
    return redirect(url_for('show_movie', movie_id=movie_id))

@app.route('/actors/<int:actor_id>/edit', methods=['GET'])
def edit_actor(actor_id):
  form = ActorForm(request.form)
  actor = Actor.query.get(actor_id)
  actor = actor.to_dict()
  form = ActorForm(formdata=None, data=actor)
  return render_template('forms/edit_actor.html', form=form, actor=actor)

@app.route('/actors/<int:actor_id>/edit', methods=['POST'])
def edit_actor_submission(actor_id):
  actor = Actor.query.get(actor_id)
  form = ActorForm(request.form, meta={'csrf': False})
  if not form.validate():
    message = []
    for field, err in form.errors.items():
      message.append(field + ' - ' + '|'.join(err))
    flash('Errors ' + str(message))
    return redirect(url_for('edit_actor_submission', actor_id=actor_id))
  else:
    try:
      actor.name = form.name.data
      actor.age = form.age.data
      actor.gender = form.gender.data
      actor.image_link = form.image_link.data
      db.session.commit()
      flash('Actor: {0} updated successfully'.format(actor.name))
    except Exception as err:
      db.session.rollback()
      print(sys.exc_info())
      flash('An error occurred updating the Actor: {0}. Error: {1}'.format(actor.name, err))
    finally:
      db.session.close()
    return redirect(url_for('show_actor', actor_id=actor_id))

#  Create Movie
#  ----------------------------------------------------------------

@app.route('/movies/create', methods=['GET'])
def create_movie_form():
  form = MovieForm()
  return render_template('forms/new_movie.html', form=form)

@app.route('/movies/create', methods=['POST'])
def create_movie_submission():
  form = MovieForm(request.form, meta={'csrf': False})
  if not form.validate():
    message = []
    for field, err in form.errors.items():
      message.append(field + ' - ' + '|'.join(err))
    flash('Errors ' + str(message))
    return redirect(url_for('create_movie_submission'))
  else:
    try:
      movie = Movie()
      movie.title = form.title.data
      movie.release_date = form.release_date.data
      movie.image_link = form.image_link.data

      db.session.add(movie)
      db.session.commit()
      flash('Movie: {0} created successfully'.format(movie.title))
    except Exception as err:
      db.session.rollback()
      print(sys.exc_info())
      flash('An error occurred creating the Movie: {0}. Error: {1}'.format(movie.title, err))
    finally:
      db.session.close()
    return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''