import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the Casting Agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.JWT = os.getenv("JWT", "")
        self.AUTH_HEADER = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.JWT),
        }
        DB_HOST = os.getenv("DB_HOST_TEST", "localhost:5432")
        DB_NAME = os.getenv("DB_NAME_TEST", "casting_agency_test")
        DB_USER = os.getenv("DB_USER_TEST", "postgres")
        DB_PASSWORD = os.getenv("DB_PASSWORD_TEST", "1")
        DB_PATH = "postgresql://{}:{}@{}/{}".format(
            DB_USER, DB_PASSWORD, DB_HOST, DB_NAME
        )

        setup_db(self.app, DB_PATH)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_home_page_200(self):
        """
        Test getting home page successfully
        """
        res = self.client().get("/")

        self.assertEqual(res.status_code, 200)

    def test_get_actors_200(self):
        """
        Test getting actors successfully
        """
        res = self.client().get("/actors", headers=self.AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actors"])

    def test_get_actors_401(self):
        """
        Test getting actors without authorization
        """
        res = self.client().get("/actors", headers="")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["message"]["code"], "authorization_header_missing")

    def test_get_movie_200(self):
        """
        Test getting movies successfully
        """
        res = self.client().get("/movies", headers=self.AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movies"])

    def test_get_movies_401(self):
        """
        Test getting movies without authorization
        """
        res = self.client().get("/movies", headers="")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["message"]["code"], "authorization_header_missing")

    def test_get_actor_by_id_200(self):
        """
        Test getting actor by id successfully
        """
        res = self.client().get("/actors/1", headers=self.AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actor"])

    def test_get_actor_by_id_401(self):
        """
        Test getting actor by id without authorization
        """
        res = self.client().get("/actors/1", headers="")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["message"]["code"], "authorization_header_missing")

    def test_get_movie_by_id_200(self):
        """
        Test getting movie by id successfully
        """
        res = self.client().get("/movies/1", headers=self.AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movie"])

    def test_get_movie_by_id_401(self):
        """
        Test getting movie by id without authorization
        """
        res = self.client().get("/movies/1", headers="")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["message"]["code"], "authorization_header_missing")

    def test_search_actors_200(self):
        """
        Test searching actors successfully
        """
        search_data = {"search_term": "Tom"}

        res = self.client().post(
            "/actors/search", headers=self.AUTH_HEADER, json=search_data
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["actors"]))

    def test_search_actors_401(self):
        """
        Test searching for actor without authorization
        """
        search_data = {"search_term": "Tom"}

        res = self.client().post("/actors/search", headers="", json=search_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["message"]["code"], "authorization_header_missing")

    def test_search_movie_200(self):
        """
        Test searching movie successfully
        """
        search_data = {"search_term": "Avengers"}

        res = self.client().post(
            "/movies/search", headers=self.AUTH_HEADER, json=search_data
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["movies"]))

    def test_search_movie_401(self):
        """
        Test searching for movie without authorization
        """
        search_data = {"search_term": "Avengers"}

        res = self.client().post("/actors/search", headers="", json=search_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["message"]["code"], "authorization_header_missing")

    def test_add_new_actor_200(self):
        actor_info = {
            "name": "Jackie Chan",
            "age": 69,
            "gender": "Male",
            "image_link": "",
        }

        res = self.client().post(
            "/actors/create", json=actor_info, headers=self.AUTH_HEADER
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_add_new_actor_401(self):
        actor_info = {
            "name": "Jackie Chan",
            "age": 69,
            "gender": "Male",
            "image_link": "",
        }

        res = self.client().post("/actors/create", json=actor_info, headers="")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["message"]["code"], "authorization_header_missing")

    def test_add_new_movie_200(self):
        info = {
            "title": "New movie",
            "release_date": "31/05/2023",
            "image_link": "",
        }

        res = self.client().post("/movies/create", json=info, headers=self.AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_add_new_movie_401(self):
        info = {
            "title": "New movie",
            "release_date": "31/05/2023",
            "image_link": "",
        }

        res = self.client().post("/movies/create", json=info, headers="")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["message"]["code"], "authorization_header_missing")

    def test_update_actor_200(self):
        info = {
            "name": "Tom Cruise 1",
            "age": 61,
            "gender": "Male",
            "image_link": "",
        }
        res = self.client().post("/actors/1/edit", json=info, headers=self.AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actor"])

    def test_update_actor_405(self):
        info = {
            "name": "Tom Cruise 1",
            "age": 61,
            "gender": "Male",
            "image_link": "",
        }
        # Link need to be wrong here
        res = self.client().post("/actors/1", json=info, headers=self.AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["message"], "method not allowed")

    def test_update_movie_200(self):
        info = {
            "title": "Avengers: Endgame",
            "release_date": "01/06/2023",
            "image_link": "",
        }
        res = self.client().post("/movies/1/edit", json=info, headers=self.AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movie"])

    def test_update_movie_405(self):
        info = {
            "title": "Avengers: Endgame",
            "release_date": "01/06/2023",
            "image_link": "",
        }
        # Link need to be wrong here
        res = self.client().post("/movies/1", json=info, headers=self.AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["message"], "method not allowed")

    def test_delete_actor_401(self):
        res = self.client().delete("/actors/2", headers="")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["message"]["code"], "authorization_header_missing")

    def test_delete_movie_401(self):
        res = self.client().delete("/movies/2", headers="")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["message"]["code"], "authorization_header_missing")

    def test_delete_actor_200(self):
        res = self.client().delete("/actors/2", headers=self.AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["actor_id"], "2")

    def test_delete_movie_200(self):
        res = self.client().delete("/movies/2", headers=self.AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["movie_id"], "2")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
