from models import *

## clear current existing database and make a clean copy ##
db.drop_all()
db.create_all()

DEMO_USER = {
    "username": "testuser",
    "password": "testpw123",
    "img_url": "https://cdn.icon-icons.com/icons2/1378/PNG/512/avatardefault_92824.png",
    "first_name": "John",
    "last_name": "Smith",
    "email": "johnsmith@gmail.com"
}

## Create a demo user and push it into the database ##
user = User.register(**DEMO_USER)
db.session.add(user)
db.session.commit()

