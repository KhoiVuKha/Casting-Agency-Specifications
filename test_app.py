import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the Casting Agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.JWT = os.getenv("JWT", "")
        self.AUTH_HEADER = {"Authorization": "Bearer {}".format(self.JWT)}
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

    def test_get_movies_200(self):
        """
        Test getting movies successfully
        """
        res = self.client().get("/movies", headers=self.AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["movies"]))


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
