# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import (
    Flask,
    render_template,
    request,
    Response,
    flash,
    redirect,
    url_for,
    jsonify,
    abort,
)
from flask_moment import Moment
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
import collections
import collections.abc

collections.Callable = collections.abc.Callable
import sys, os
from operator import itemgetter  # for sorting lists of tuples

# import database's models
from models import db, setup_db, Actor, Movie

ITEMS_PER_PAGE = 10


def paginate_items(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE

    items = [items.format() for item in selection]
    current_items = items[start:end]

    return current_items


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    moment = Moment(app)
    setup_db(app)

    # Set up CORS. Allow '*' for origins.
    CORS(app)

    # Use the after_request decorator to set Access-Control-Allow
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization"
        )
        response.headers.add(
            "Access-Control-Allow-Headers", "GET, POST, PATCH, DELETE, OPTIONS"
        )
        return response

    # ----------------------------------------------------------------------------#
    # Controllers.
    # ----------------------------------------------------------------------------#

    # Home
    @app.route("/")
    def index():
        return render_template("pages/home.html")

    # Get actors
    # ----------------------------------------------------------------
    @app.route("/actors")
    def actors():
        data = Actor.query.order_by(Actor.id).all()

        if request.headers.get("Content-Type") == "application/json":
            return jsonify(
                {"success": True, "actors": [actor.to_dict() for actor in data]}
            )
        return render_template("pages/actors.html", actors=data)

    # Search for an actor
    # ----------------------------------------------------------------
    @app.route("/actors/search", methods=["POST"])
    def search_actors():
        if request.headers.get("Content-Type") == "application/json":
            body = request.get_json()
            search_term = body.get("search_term", None)
        else:
            search_term = request.form.get("search_term", "").strip()

        if search_term:
            results = Actor.query.filter(
                Actor.name.ilike("%{}%".format(search_term))
            ).all()

            actor_list = []
            for actor in results:
                actor_list.append(
                    {"id": actor.id, "name": actor.name, "num_movies": None}
                )

            response = {"count": len(results), "data": actor_list}

            if request.headers.get("Content-Type") == "application/json":
                return jsonify(
                    {
                        "success": True,
                        "total": len(results),
                        "actors": [actor.to_dict() for actor in results],
                    }
                )

            return render_template(
                "pages/search_actors.html",
                results=response,
                search_term=request.form.get("search_term", ""),
            )
        else:
            abort(404)  # Actor searching not found

    # Shows the actor page with the given actor_id
    # ----------------------------------------------------------------
    @app.route("/actors/<int:actor_id>")
    def show_actor(actor_id):
        try:
            actor = Actor.query.get(actor_id)
            data = actor.to_dict()

            # movies = list(Actor.movies)
            # movie_count = len(movies)
            # data["movie_count"] = movie_count
            if request.headers.get("Content-Type") == "application/json":
                return jsonify(
                    {
                        "success": True,
                        "actor": [data],
                    }
                )
            # @todo: refactor the page
            return render_template("pages/show_actor.html", actor=data)
        except:
            abort(422)  # Unprocessable

    # Create Actor
    # ----------------------------------------------------------------
    @app.route("/actors/create", methods=["GET"])
    def create_actor_form():
        # @todo: refactor
        form = ActorForm(request.form, meta={"csrf": False})
        return render_template("forms/new_actor.html", form=form)

    @app.route("/actors/create", methods=["POST"])
    def create_actor_submission():
        actor = Actor()
        if request.headers.get("Content-Type") == "application/json":
            body = request.get_json()
            actor.name = body.get("name", None)
            actor.age = body.get("age", None)
            actor.gender = body.get("gender", None)
            actor.image_link = body.get("image_link", None)
        else:
            form = ActorForm(request.form, meta={"csrf": False})
            if not form.validate():
                message = []
                for field, err in form.errors.items():
                    message.append(field + " - " + "|".join(err))
                flash("Errors " + str(message))
                return redirect(url_for("create_actor_submission"))

            actor.name = form.name.data
            actor.age = form.age.data
            actor.gender = form.gender.data
            actor.image_link = form.image_link.data
        try:
            # Insert new actor to database
            actor.insert()
            flash("Actor: {0} created successfully!".format(actor.name))

            # Get list of actors after insert
            selection = Actor.query.all()

        except Exception as err:
            db.session.rollback()
            flash(
                "An error occurred creating the Actor: {0}. Error: {1}".format(
                    actor.name, err
                )
            )
            print(sys.exc_info())
            abort(500)  # Internal server error
        finally:
            db.session.close()

        if request.headers.get("Content-Type") == "application/json":
            return jsonify(
                {
                    "success": True,
                    "actor": [actor.to_dict()],
                    "total": len(selection),
                }
            )
        return render_template("pages/home.html")

    # Delete actor
    # ----------------------------------------------------------------
    @app.route("/actors/<actor_id>", methods=["DELETE"])
    def delete_actor(actor_id):
        try:
            actor = Actor.query.get(actor_id)
            actor_name = actor.name

            # Delete the selected actor
            actor.delete()
            flash("Successfully removed actor {0}.".format(actor_name))
        except Exception as err:
            db.session.rollback()
            flash(
                "An error occurred removing the Actor: {0}. Error: {1}".format(
                    actor_name, err
                )
            )
            abort(500)  # Internal server error
        finally:
            db.session.close()
        return jsonify({"success": True, "actor_id": actor_id})

    # Update actor
    # ----------------------------------------------------------------
    @app.route("/actors/<int:actor_id>/edit", methods=["GET"])
    def edit_actor(actor_id):
        form = ActorForm(request.form)
        actor = Actor.query.get(actor_id)
        actor = actor.to_dict()
        form = ActorForm(formdata=None, data=actor)
        return render_template("forms/edit_actor.html", form=form, actor=actor)

    @app.route("/actors/<int:actor_id>/edit", methods=["POST"])
    def edit_actor_submission(actor_id):
        actor = Actor.query.get(actor_id)
        if request.headers.get("Content-Type") == "application/json":
            body = request.get_json()
            actor.name = body.get("name", None)
            actor.age = body.get("age", None)
            actor.gender = body.get("gender", None)
            actor.image_link = body.get("image_link", None)
        else:
            print("aaaaa")
            form = ActorForm(request.form, meta={"csrf": False})
            if not form.validate():
                message = []
                for field, err in form.errors.items():
                    message.append(field + " - " + "|".join(err))
                flash("Errors " + str(message))
                return redirect(url_for("edit_actor_submission", actor_id=actor_id))

            actor.name = form.name.data
            actor.age = form.age.data
            actor.gender = form.gender.data
            actor.image_link = form.image_link.data

        try:
            # Update actor info to database
            actor.update()
            flash("Actor: {0} updated successfully".format(actor.name))
        except Exception as err:
            db.session.rollback()
            print(sys.exc_info())
            flash(
                "An error occurred updating the Actor: {0}. Error: {1}".format(
                    actor.name, err
                )
            )
            abort(500)  # Internal server error
        finally:
            db.session.close()

        if request.headers.get("Content-Type") == "application/json":
            return jsonify(
                {
                    "success": True,
                    "actor": [actor.to_dict()],
                }
            )
        return redirect(url_for("show_actor", actor_id=actor_id))

    # Get Movies
    # ----------------------------------------------------------------
    @app.route("/movies")
    def movies():
        data = Movie.query.order_by(Movie.id).all()

        if request.headers.get("Content-Type") == "application/json":
            return jsonify(
                {"success": True, "movies": [movie.to_dict() for movie in data]}
            )
        return render_template("pages/movies.html", movies=data)

    # Search for an movie
    # ----------------------------------------------------------------
    @app.route("/movies/search", methods=["POST"])
    def search_movies():
        if request.headers.get("Content-Type") == "application/json":
            body = request.get_json()
            search_term = body.get("search_term", None)
        else:
            search_term = request.form.get("search_term", "").strip()

        if search_term:
            results = Movie.query.filter(
                Movie.title.ilike("%{}%".format(search_term))
            ).all()

            movie_list = []
            for movie in results:
                movie_list.append(
                    {
                        "id": movie.id,
                        "title": movie.title,
                        "release_date": movie.release_date,
                        "image_link": movie.image_link,
                        "actors": None,  # @todo
                    }
                )

            response = {"count": len(movie_list), "data": movie_list}

            if request.headers.get("Content-Type") == "application/json":
                return jsonify(
                    {
                        "success": True,
                        "total": len(results),
                        "movies": [movie.to_dict() for movie in results],
                    }
                )
            return render_template(
                "pages/search_movies.html",
                results=response,
                search_term=request.form.get("search_term", ""),
            )
        else:
            abort(404)  # Not found

    # Show movie by ID
    # ----------------------------------------------------------------
    @app.route("/movies/<int:movie_id>")
    def show_movie(movie_id):
        try:
            movie = Movie.query.get(movie_id)
            data = movie.to_dict()

            if request.headers.get("Content-Type") == "application/json":
                return jsonify(
                    {
                        "success": True,
                        "movie": [data],
                    }
                )
            return render_template("pages/show_movie.html", movie=data)
        except:
            abort(422)  # Unprocessable

    # Create Movie
    # ----------------------------------------------------------------
    @app.route("/movies/create", methods=["GET"])
    def create_movie_form():
        form = MovieForm(request.form, meta={"csrf": False})
        return render_template("forms/new_movie.html", form=form)

    @app.route("/movies/create", methods=["POST"])
    def create_movie_submission():
        movie = Movie()
        if request.headers.get("Content-Type") == "application/json":
            body = request.get_json()
            movie.title = body.get("title", None)
            movie.release_date = body.get("release_date", None)
            movie.image_link = body.get("image_link", None)
        else:
            form = MovieForm(request.form, meta={"csrf": False})

            if not form.validate():
                message = []
                for field, err in form.errors.items():
                    message.append(field + " - " + "|".join(err))
                flash("Errors " + str(message))
                return redirect(url_for("create_movie_submission"))

            movie.title = form.title.data
            movie.release_date = form.release_date.data
            movie.image_link = form.image_link.data
        try:
            # Insert new movie to database
            movie.insert()
            flash("Movie: {0} created successfully".format(movie.title))

            # Get list of movies after insert
            selection = Movie.query.all()
        except Exception as err:
            db.session.rollback()
            print(sys.exc_info())
            flash(
                "An error occurred creating the Movie: {0}. Error: {1}".format(
                    movie.title, err
                )
            )
            abort(500)  # Internal server error
        finally:
            db.session.close()

        if request.headers.get("Content-Type") == "application/json":
            return jsonify(
                {"success": True, "movie": [movie.to_dict()], "total": len(selection)}
            )
        return render_template("pages/home.html")  # Delete movie

    # ----------------------------------------------------------------
    @app.route("/movies/<movie_id>", methods=["DELETE"])
    def delete_movie(movie_id):
        try:
            movie = Movie.query.get(movie_id)
            movie_title = movie.title

            # Delete selected movie from database
            movie.delete()
            flash("Successfully removed movie {0}.".format(movie_title))
        except Exception as err:
            db.session.rollback()
            flash(
                "An error occurred removing the Movie: {0}. Error: {1}".format(
                    movie_title, err
                )
            )
            abort(500)  # Internal server error
        finally:
            db.session.close()
        return jsonify({"success": True, "movie_id": movie_id})

    # Update movie
    # ----------------------------------------------------------------
    @app.route("/movies/<int:movie_id>/edit", methods=["GET"])
    def edit_movie(movie_id):
        form = MovieForm(request.form)
        movie = Movie.query.get(movie_id)
        movie = movie.to_dict()
        form = MovieForm(formdata=None, data=movie)
        return render_template("forms/edit_movie.html", form=form, movie=movie)

    @app.route("/movies/<int:movie_id>/edit", methods=["POST"])
    def edit_movie_submission(movie_id):
        movie = Movie.query.get(movie_id)
        if request.headers.get("Content-Type") == "application/json":
            body = request.get_json()
            movie.title = body.get("title", None)
            movie.release_date = body.get("release_date", None)
            movie.image_link = body.get("image_link", None)
        else:
            form = MovieForm(request.form, meta={"csrf": False})
            if not form.validate():
                message = []
                for field, err in form.errors.items():
                    message.append(field + " - " + "|".join(err))
                flash("Errors " + str(message))
                return redirect(url_for("edit_movie_submission", movie_id=movie_id))

            movie.title = form.title.data
            movie.release_date = form.release_date.data
            movie.image_link = form.image_link.data
        try:
            # Update movie info to database
            movie.update()
            flash("Movie: {0} updated successfully".format(movie.title))
        except Exception as err:
            db.session.rollback()
            print(sys.exc_info())
            flash(
                "An error occurred updating the Movie: {0}. Error: {1}".format(
                    movie.title, err
                )
            )
            abort(500)  # Internal server error
        finally:
            db.session.close()

        if request.headers.get("Content-Type") == "application/json":
            return jsonify({"success": True, "movie": [movie.to_dict()]})
        return redirect(url_for("show_movie", movie_id=movie_id))

    # Error Handlers
    # ----------------------------------------------------------------

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({"success": False, "error": 401, "message": "unathorized"}), 401

    @app.errorhandler(404)
    def not_found(error):
        # Render the HTML template
        html = render_template("errors/404.html"), 404

        # Return the JSON data
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(405)
    def method_not_allowed(error):
        return (
            jsonify({"success": False, "error": 405, "message": "method not allowed"}),
            405,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(500)
    def internal_server_error(error):
        # Render the HTML template
        html = render_template("errors/500.html"), 500

        # Return the JSON data
        return (
            jsonify(
                {"success": False, "error": 500, "message": "internal server error"}
            ),
            500,
        )

    if not app.debug:
        file_handler = FileHandler("error.log")
        file_handler.setFormatter(
            Formatter(
                "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
            )
        )
        app.logger.setLevel(logging.INFO)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.info("errors")

    return app


# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#
app = create_app()

# Default port:
if __name__ == "__main__":
    app.run()
