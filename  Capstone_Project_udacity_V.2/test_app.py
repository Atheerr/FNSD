import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actor, Movie
# from models import setup_db, Actor, Movie, db_insert_all


class CastingAgencyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        # self.database_path = "postgres:///m_db"
        self.database_path = "postgres://qmuctnxsjzynmq:caaa92f73f104bc8eaf93ab5b71a13adec2d14616f4eac78575a109a0a6e4896@ec2-52-70-67-123.compute-1.amazonaws.com:5432/d5o744grfo2435"
        setup_db(self.app, self.database_path)
        # db_insert_all()

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()
            # Tokens
            self.casting_assistant_auth = os.environ.get('ASSISTANT_TOKEN')
            self.casting_director_auth = os.environ.get('DIRECTOR_TOKEN')
            self.producer_auth = os.environ.get('PRODUCER_TOKEN')
            # test data 
            self.new_actor = {
                'name': 'Test Nmae',
                'age': '27',
                'gender': 'Female'
            }
            self.new_movie = {
                'title': 'Test Movie',
                'release_date': '21/06/1993'
            }
            self.emty_actor = {}
            self.emty_movie = {}

    def tearDown(self):
        pass
# ----------------------------------------------------------------------------
# -------------------------      Test       ----------------------------------
#     Test for success/failure at each endpoint with permissions
# ----------------------------------------------------------------------------
    # Test for first page = success

    def test_first(self):
        res = self.client().get('/')
        self.assertEqual(res.status_code, 200)

    # Test for retrieve actors = success
    def test_retrieve_actors_valid(self):
        res = self.client().get(
            '/actors',
            headers={
                "Authorization": "Bearer {}".format(
                    self.producer_auth)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    # Test for retrieve movies = success
    def test_retrieve_movies_valid(self):
        res = self.client().get(
            '/movies',
            headers={
                "Authorization": "Bearer {}".format(
                    self.producer_auth)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    # Test for create actor = success
    def test_create_actor_valid(self):
        res = self.client().post(
            '/actors',
            json=self.new_actor,
            headers={
                "Authorization": "Bearer {}".format(
                    self.producer_auth)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Test for create actor = failure
    def test_create_actor_unvalid(self):
        res = self.client().post(
            '/actors',
            json=self.emty_actor,
            headers={
                "Authorization": "Bearer {}".format(
                    self.producer_auth)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    # Test for create movies = success
    def test_create_movie_valid(self):
        res = self.client().post(
            '/movies',
            json=self.new_movie,
            headers={
                "Authorization": "Bearer {}".format(
                    self.producer_auth)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Test for create movies = failure
    def test_create_movie_unvalid(self):
        res = self.client().post(
            '/movies',
            json=self.emty_movie,
            headers={
                "Authorization": "Bearer {}".format(
                    self.producer_auth)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    # Test for update actor = success
    def test_update_actor_valid(self):
        res = self.client().patch(
            '/actors/1',
            json=self.new_actor,
            headers={
                "Authorization": "Bearer {}".format(
                    self.producer_auth)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Test for update actor = failure
    def test_update_actor_unvalid(self):
        res = self.client().patch(
            '/actors/1',
            json=self.emty_actor,
            headers={
                "Authorization": "Bearer {}".format(
                    self.producer_auth)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    # Test for update movie = success
    def test_update_movie_valid(self):
        res = self.client().patch(
            '/movies/1',
            json=self.new_movie,
            headers={
                "Authorization": "Bearer {}".format(
                    self.producer_auth)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Test for update movies = failure
    def test_update_movie_unvalid(self):
        res = self.client().patch(
            '/movies/1',
            json=self.emty_movie,
            headers={
                "Authorization": "Bearer {}".format(
                    self.producer_auth)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    # Test for delete actor = success
    def test_delete_actor_valid(self):
        res = self.client().delete(
            '/actors/1',
            headers={
                "Authorization": "Bearer {}".format(
                    self.producer_auth)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 1)

    # Test for delete actor = failure
    def test_delete_actor_unvalid(self):
        res = self.client().delete(
            '/actors/400',
            headers={
                "Authorization": "Bearer {}".format(
                    self.producer_auth)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    # Test for delete movies = success
    def test_delete_movie_valid(self):
        res = self.client().delete(
            '/movies/1',
            headers={
                "Authorization": "Bearer {}".format(
                    self.producer_auth)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 1)

    # Test for delete movies = failure
    def test_delete_movie_unvalid(self):
        res = self.client().delete(
            '/movies/123',
            headers={
                "Authorization": "Bearer {}".format(
                    self.producer_auth)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    # Test for casting assistant auth = success
    def test_casting_assistant_auth_valid(self):
        res = self.client().get(
            '/actors',
            headers={
                "Authorization": "Bearer {}".format(
                    self.casting_assistant_auth)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    # Test for casting assistant auth = failure
    def test_casting_assistant_auth_unvalid(self):
        res = self.client().patch(
            '/movies/1',
            json=self.new_movie,
            headers={
                "Authorization": "Bearer {}".format(
                    self.casting_assistant_auth)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unauthorized")

    # Test for casting director auth = success
    def test_casting_director_auth_valid(self):
        res = self.client().get(
            '/actors',
            headers={
                "Authorization": "Bearer {}".format(
                    self.casting_director_auth)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    # Test for casting director auth = failure
    def test_casting_director_auth_unvalid(self):
        res = self.client().delete(
            '/movies/1',
            headers={
                "Authorization": "Bearer {}".format(
                    self.casting_director_auth)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unauthorized")


if __name__ == "__main__":
    unittest.main()
