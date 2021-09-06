import os
# from flask import Flask, request, abort, jsonify
from flask import (
  Flask,
  request,
  jsonify,
  abort
)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth import AuthError, requires_auth
from models import setup_db, Actor, Movie, db
# from models import setup_db, db_insert_all,Actor, Movie, db


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    # db_insert_all()
    CORS(app)

# ----------------------------------------------------------------------------
# -------------------------      Route      ----------------------------------
# ----------------------------------------------------------------------------

    @app.route('/')
    def retrieve_first():
        return " Welcome to my last project 'Casting Agency' ... I am very happy that you visit us "

# ----------------------------------------------------------------------------
# -------------------------      Route Actors  -------------------------------
# ----------------------------------------------------------------------------

    # GET Actors
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(self):
        selection = Actor.query.order_by(Actor.id).all()
        if len(selection) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'actors': [actor.format() for actor in selection]
        }), 200

    # POST Actors
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def post_actor(self):
        body = request.get_json()
        new_name = body.get('name', None)
        new_age = body.get('age', None)
        new_gender = body.get('gender', None)
        if ((new_name is None) or (new_age is None) or (new_gender is None)):
            abort(422)
        try:
            actor = Actor(name=new_name, gender=new_gender, age=new_age)
            actor.insert()

            return jsonify({
                'success': True,
                'created': actor.id
            }), 200

        except BaseException:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

    # PATCH Actors
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def patch_actor(self, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if actor is None:
            abort(404)
        body = request.get_json()
        new_name = body.get('name', None)
        new_age = body.get('age', None)
        new_gender = body.get('gender', None)

        if ((new_name is None) and (new_age is None) and (new_gender is None)):
            abort(422)
        try:
            if new_name is not None:
                actor.name = new_name
            if new_age is not None:
                actor.age = new_age
            if new_gender is not None:
                actor.gender = new_gender

            actor.update()

            return jsonify({
                'success': True,
                'actor': actor.format()
            }), 200

        except BaseException:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

    # DELETE Actors
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(self, actor_id):
        try:
            actor = Actor.query.filter(
                Actor.id == actor_id).one_or_none()

            if actor is None:
                abort(404)

            actor.delete()

            return jsonify({
                'success': True,
                'delete': actor.id
            }), 200
        except BaseException:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

# ----------------------------------------------------------------------------
# -------------------------      Route Actors  -------------------------------
# ----------------------------------------------------------------------------
    # GET Movies
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(self):
        selection = Movie.query.order_by(Movie.id).all()
        if len(selection) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'movies': [movie.format() for movie in selection]
        }), 200

    # POST Movies
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def post_movie(self):
        body = request.get_json()
        new_title = body.get('title', None)
        new_release_date = body.get('release_date', None)

        if ((new_title is None) or (new_release_date is None)):
            abort(422)
        try:
            movie = Movie(title=new_title, release_date=new_release_date)
            movie.insert()

            return jsonify({
                'success': True,
                'created': movie.id
            }), 200

        except BaseException:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

    # PATCH Movies
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def patch_movie(self, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)
        body = request.get_json()
        new_title = body.get('title', None)
        new_release_date = body.get('release_date', None)
        if ((new_title is None) and (new_release_date is None)):
            abort(422)
        try:
            if new_title is not None:
                movie.title = new_title
            if new_release_date is not None:
                movie.release_date = new_release_date
            movie.update()
            return jsonify({
                'success': True,
                'movie': movie.format()
            }), 200
        except BaseException:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

    # Delete Movies
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(self, movie_id):
        try:
            movie = Movie.query.filter(
                Movie.id == movie_id).one_or_none()
            if movie is None:
                abort(404)
            movie.delete()
            return jsonify({
                'success': True,
                'delete': movie.id
            }), 200
        except BaseException:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

# ----------------------------------------------------------------------------
# -------------------------    Error Handling  -------------------------------
# ----------------------------------------------------------------------------

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource Not Found"
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(401)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "unauthorized"
        }), 401

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    @app.errorhandler(AuthError)
    def authentication_error(ex):
        return jsonify({
            "success": False,
            "error": ex.status_code,
            "message": ex.error['code']
        }), ex.status_code
    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
