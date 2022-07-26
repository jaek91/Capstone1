from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

user_img_default = "https://cdn.icon-icons.com/icons2/1378/PNG/512/avatardefault_92824.png"


def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """Description of site user."""

    __tablename__ = "users"

    username = db.Column(db.String(75), nullable=False,
                         primary_key=True, 
                         unique=True)

    password = db.Column(db.Text, 
                         nullable=False)
    
    img_url = db.Column(db.Text, 
                         nullable= True, default= user_img_default)

    first_name = db.Column(db.String(75), nullable=False)

    last_name = db.Column(db.String(75), nullable=False)

    email = db.Column(db.String(100), nullable=False)

    favorites = db.relationship("Favorites", backref="user", cascade="all,delete")
    watched = db.relationship("Watched", backref="user", cascade="all,delete")
    to_watch = db.relationship("ToWatch", backref="user", cascade="all,delete")

    # method to register a user 
    @classmethod
    def register(cls, username, password, first_name, last_name, email, img_url):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(password)
        
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        if img_url is None:
           img_url = user_img_default

        user = cls(username = username, password = hashed_utf8, 
        first_name = first_name, last_name = last_name, email = email, img_url = img_url)
        
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists & password is correct.
           Return user if valid; else return False."""

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            # return user instance if they're validated
            return user
        else:
            return False

class Favorites(db.Model):
    """Description of favorites list for user"""

    __tablename__ = "favorites"

    id = db.Column(db.Integer, primary_key = True, autoincrement=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(75), db.ForeignKey("users.username"), nullable=False)
    # watched = db.Column(db.Text, db.ForeignKey("watched.id"), nullable= True)

    @classmethod
    def create(cls, name, description, username):

        entry = cls(name = name, description = description, username = username)
        return entry

class Watched(db.Model):
    """Description of watched list for user"""

    __tablename__ = "watched"

    id = db.Column(db.Integer, primary_key = True, autoincrement=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(75), db.ForeignKey("users.username"), nullable=False)
    # favorites = db.Column(db.Text, db.ForeignKey("favorites.id"), nullable= True )

    @classmethod
    def create(cls, name, description, username):
        entry = cls(name = name, description = description, username = username)
        return entry

class ToWatch(db.Model):
    """Description of to-watch list for user"""

    __tablename__ = "to_watch"

    id = db.Column(db.Integer, primary_key = True, autoincrement=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(75), db.ForeignKey("users.username"), nullable=False)

    @classmethod
    def create(cls, name, description, username):
        entry = cls(name = name, description = description, username = username)
        return entry