from unittest import TestCase

from app import app
from models import db, User, Favorites, Watched, ToWatch

import requests
import json


# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///anime_db_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

TEST_USER = {
    "username": "testuser1",
    "password": "testpw123",
    "img_url": "https://cdn.icon-icons.com/icons2/1378/PNG/512/avatardefault_92824.png",
    "first_name": "John",
    "last_name": "Smith",
    "email": "johnsmith@test.com"
}

TEST_ANIME = {
    "title": "Violet Evergarden",
    "synopsis": "There are words Violet heard on the battlefield, which she cannot forget. These words were given to her by someone she holds dear, more than anyone else. She does not yet know their meaning.\nA certain point in time, in the continent of Telesis. The great war which divided the continent into North and South has ended after four years, and the people are welcoming a new generation.\n\nViolet Evergarden, a young girl formerly known as “the weapon”, has left the battlefield to start a new life at CH Postal Service. There, she is deeply moved by the work of “Auto Memories Dolls”, who carry people's thoughts and convert them into words.\n\nViolet begins her journey as an Auto Memories Doll, and comes face to face with various people's emotions and differing shapes of love. All the while searching for the meaning of those words.\n\n(Source: Anime Expo)",
}

## this is the actual anime id of our test fav anime Violet Evergarden as retrieved from Kitsu API call
TEST_ANIME_ID = {
    "id": "12230"
}

class UserMethodsTestCase(TestCase):
    """Tests for various User class methods"""

    db.drop_all()
    db.create_all()

    def setUp(self):
        User.query.delete()
        user = User.register(**TEST_USER)
        db.session.add(user)
        db.session.commit()
        self.user = user
        # self.username = user.username

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()

    def test_authentication_valid_pw(self):
        """This test serves to test the authenticate method in the User class 
        in that a valid password results in returning the user"""
        valid_pw = "testpw123"
        auth_response = User.authenticate(self.user.username, valid_pw)
        self.assertEqual(auth_response, self.user)
    
    def test_authentication_invalid_pw(self):
        """This test serves to test the authenticate method in the User class 
        in that a invalid password results in returning False"""
        random_pw = "random123"
        auth_response = User.authenticate(self.user.username, random_pw)
        self.assertEqual(auth_response, False)


class AddAnimesTest(TestCase):

    db.drop_all()
    db.create_all()

    def setUp(self):
        User.query.delete()
        user = User.register(**TEST_USER)
        db.session.add(user)
        db.session.commit()
        self.user = user

    def tearDown(self):
        """Clean up fouled transactions."""
        db.session.rollback()

    # def login(self):
    #     with app.test_client() as client:
    #         client.post('/login', data={
    #             "username": "testuser1",
    #             "password": "testpw123",
    #         })

    def test_add_to_favorites(self):
        """Call the API with values-> get user check entry is not in favorites -> call API"""

        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['username'] = self.user.username

            response = client.post("/users/favorites/add", data= json.dumps(TEST_ANIME_ID), 
                        headers={'Content-Type': 'application/json', 'Data-Type': 'text'})
            
            ##check that we get the return value from hitting the /users/favorites/add route ##
            self.assertEqual(response.status_code, 204) 

            new_fav_anime_name = Favorites.query.with_entities(Favorites.name).filter_by(username = self.user.username).first()[0]
            
            ##check that test anime title (i.e. Violet Evergarden) in the database exists
            self.assertEqual(TEST_ANIME["title"], new_fav_anime_name)
    
    def test_add_to_watch(self):
        """Call the API with values-> get user check entry is not in favorites -> call API"""

        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['username'] = self.user.username

            response = client.post("/users/towatch/add", data= json.dumps(TEST_ANIME_ID), 
                        headers={'Content-Type': 'application/json', 'Data-Type': 'text'})
            
            ##check that we get the expected return value from hitting the /users/towatch/add route ##
            self.assertEqual(response.status_code, 204) 

            new_towatch_anime_name = ToWatch.query.with_entities(ToWatch.name).filter_by(username = self.user.username).first()[0]
            
            ##check that test anime title (i.e. Violet Evergarden) in the database exists
            self.assertEqual(TEST_ANIME["title"], new_towatch_anime_name)
    
    def test_add_to_watched(self):
        """Call the API with values-> get user check entry is not in favorites -> call API"""

        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['username'] = self.user.username

            response = client.post("/users/watched/add", data= json.dumps(TEST_ANIME_ID), 
                        headers={'Content-Type': 'application/json', 'Data-Type': 'text'})
            
            ##check that we get the expected return value from hitting the "/users/watched/add" route ##
            self.assertEqual(response.status_code, 204) 

            new_watched_anime_name = Watched.query.with_entities(Watched.name).filter_by(username = self.user.username).first()[0]
            
            ## check that the newly added test anime title (i.e. Violet Evergarden) in the database exists
            self.assertEqual(TEST_ANIME["title"], new_watched_anime_name)