
import json
import os
from flask import Flask, render_template, redirect, session, flash, request
from models import connect_db, db, User, Favorites, Watched, ToWatch
from request_info import *
from recommendations import *
from forms import SearchForm, RegisterForm, LoginForm
from werkzeug.exceptions import Unauthorized
import random

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "postgresql:///anime_db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = os.urandom(12).hex()

connect_db(app)
db.create_all()


@app.route('/')
def home_page():
    if "username" not in session: 
        userOn = False
        return render_template("home.html", userOn = userOn)
    
    else: 
        user = User.query.get(session["username"])
        userOn = True
        return render_template("home.html", userOn = userOn, user = user)
   
    
######## User register/login/logout routes ########

@app.route('/register', methods=["GET","POST"])
def register_user():
    
    form = RegisterForm()

    ##post request for registering new user
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        img_url = form.img_url.data

        new_user = User.register(username, password, first_name, last_name, email, img_url)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = new_user.username
        flash('User Created!', 'success')
        return redirect(f'/users/{new_user.username}')
    
    ## if validation fails, we simply retrieve the registration form ##
    return render_template("users/register.html", form = form)

@app.route('/login', methods=["GET", "POST"])
def login():
    """Displays login page and logs user in"""
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username,password)

        if user:
            session["username"] = username
            return redirect(f'/users/{username}')
        else:
            form.username.errors = ["Invalid username or password!"]

    return render_template('users/login.html', form = form)
        
@app.route('/logout')
def logout():
    """Logs user out and redirects back to home page"""
    session.pop("username")
    return redirect("/")

@app.route('/users/<username>', methods=["GET"])
def display_user_info(username):
    if "username" not in session or username != session['username']:
        raise Unauthorized
    else:
        user = User.query.get(username)
       
        fav_titles = Favorites.query.with_entities(Favorites.name).filter_by(username = username).all()
        curr_db_fav_titles = [name[0] for name in fav_titles]
        processed_fav_titles = []

        if curr_db_fav_titles:
            for title in curr_db_fav_titles: 
                jp_title = convert_title_to_jp(title)
                results = give_recommendations(jp_title)
                if results is not False:
                ## we do this preprocessing because not every title in the static database for our recommendation system 
                ## that we're comparing to the user's favorites list will have a corresponding match 
                    processed_fav_titles.append(title) 
            
            ## we randomly choose a title from user's favorite's list ##
            random_title = random.choice(processed_fav_titles)
            jp_title = convert_title_to_jp(random_title)
            results = json.loads(give_recommendations(jp_title))
            suggested_titles = get_unique_titles(results, jp_title)
           
            rec_titles_info = get_info_recommended_titles(suggested_titles)
            rec_data = {"random_title": random_title, "rec_titles": rec_titles_info}
            
            return render_template('users/info.html', user = user, data = rec_data)
    return render_template('users/info.html', user = user)

@app.route('/search', methods=["GET","POST"])
def search_anime():
    form = SearchForm()

    if "username" not in session: 
        userOn = False
        if form.validate_on_submit():
            title = form.title.data
            response = get_search_results(title)
            return render_template("search_result.html", response = response, userOn = userOn)
        else:
            return render_template("search.html", userOn = userOn, form = form)

    else: 
        userOn = True
        username = session['username']
        user = User.query.get(username)
        
        if form.validate_on_submit():
            title = form.title.data
            response = get_search_results(title)
            check_anime_in_db_lists(response, username)

            return render_template("search_result.html", response = response, userOn = userOn, user = user)
        
        return render_template("search.html", userOn = userOn, form = form, user = user)

@app.route("/users/favorites/add", methods=["GET","POST"])
def add_to_favorites():

    if "username" not in session:
        raise Unauthorized
    else:
        username = session["username"]

    fav_anime_ids = get_anime_ids_db("favorites", username)

    while (len(fav_anime_ids) < 10):
        
        if request.method == "POST":    
            id = request.json['id']
            print(f"This anime to be added has an id of {id}")

            if id not in fav_anime_ids:
                anime_data = get_anime(id)
                title = anime_data["title"]
                synopsis = anime_data["synopsis"]
                new_fav = Favorites.create(title, synopsis, username)
                db.session.add(new_fav)
                db.session.commit()
                return ('', 204)
            
            return ('', 204)
            
    if (len(fav_anime_ids) >= 10):
        
        flash("You can only add 10 favorites to an favorites list!", 'warning')
        return ('',204)
        

    return ('',204)
 

@app.route("/users/<username>/favorites", methods=["GET"])
def view_favorites(username):
    if "username" not in session or username != session['username'] :
        userOn = False
        raise Unauthorized
    else:
        userOn = True

    user = User.query.get(username)

    return render_template("anime_categories/favorites.html", userOn = userOn, user = user, username = username)

@app.route("/users/towatch/add", methods=["GET","POST"])
def add_to_watch():
    if "username" not in session:
        raise Unauthorized
    else: 
        username = session["username"]
    
    towatch_anime_ids = get_anime_ids_db("towatch", username)
    watched_anime_ids = get_anime_ids_db("watched", username)

    while (len(towatch_anime_ids) < 20):
        if request.method == "POST":
            id = request.json['id']

            if id not in towatch_anime_ids and id not in watched_anime_ids:
                anime_data = get_anime(id)
                title = anime_data["title"]
                synopsis = anime_data["synopsis"]
                new_to_watch = ToWatch.create(title, synopsis, username)
                db.session.add(new_to_watch)
                db.session.commit()
                return ('',204)
            
    if (len(towatch_anime_ids) >= 20):
        return ('',204)
    


@app.route("/users/<username>/towatch", methods=["GET"])
def view_to_watch(username):
    if "username" not in session or username != session['username']:
        userOn = False
        raise Unauthorized
    else:
        userOn = True

    user = User.query.get(username)

    return render_template("anime_categories/towatch.html", userOn = userOn, user = user, username = username)

@app.route("/users/watched/add", methods=["GET","POST"])
def add_to_watched():
    if "username" not in session:
        raise Unauthorized
    else: 
        username = session["username"]

    watched_anime_ids = get_anime_ids_db("watched", username)
    towatch_anime_ids = get_anime_ids_db("towatch", username)

    while (len(watched_anime_ids) < 20):
        if request.method == "POST":
            id = request.json['id']

            if id not in watched_anime_ids or id not in towatch_anime_ids:
                anime_data = get_anime(id)
                title = anime_data["title"]
                synopsis = anime_data["synopsis"]
                new_watched = Watched.create(title, synopsis, username)
                db.session.add(new_watched)
                db.session.commit()  
                return ('',204)
            
    if (len(watched_anime_ids) >= 20):
        return ('',204)

   
@app.route("/users/<username>/watched", methods=["GET"])
def view_watched(username):
    if "username" not in session or username != session['username'] :
        userOn = False
        raise Unauthorized
    else:
        userOn = True

    user = User.query.get(username)

    return render_template("anime_categories/watched.html", userOn = userOn, user = user, username = username)

##------- DELETE ROUTES -------##

##--DELETE FAVORITES ROUTE--##
@app.route("/users/<username>/favorites/delete", methods=["GET", "POST"])
def delete_fav(username):
    if "username" not in session:
        raise Unauthorized
    
    if request.method == "POST":
        favorites_id = request.json['id']
        anime_title = request.json['title']

        anime_id = get_anime_id(anime_title)
        anime_entry = Favorites.query.get(favorites_id)
        
        fav_ids = get_anime_ids_db("favorites", username)

        print(f"This is the content of {fav_ids} before removing {anime_id}")
        
        db.session.delete(anime_entry)
        db.session.commit()
        
        final_fav_ids = list(filter(lambda x: x != anime_id, fav_ids))
    
        print(f"{final_fav_ids} should be the new latest updated favorites ids list with no more {anime_id}")
        return ('',204)

    return ('',204)

##--DELETE WATCHED ROUTE--##
@app.route("/users/<username>/watched/delete", methods=["GET", "POST"])
def delete_watched(username):
    
    if "username" not in session:
        raise Unauthorized
  
    if request.method == "POST":
        watched_id = request.json['id']
        anime_title = request.json['title']

        print(f"{anime_title} is the name of the anime to be deleted")
        print(f"{watched_id} is the anime id in the database to be deleted")
        anime_id = get_anime_id(anime_title)

        anime_entry = Watched.query.get(watched_id)        
        watched_ids = get_anime_ids_db("watched", username)
        print(f"This is the content of {watched_ids} from the database before removing {anime_id}")
        
        db.session.delete(anime_entry)
        db.session.commit()
        
        print(f"{watched_ids} should be the new latest updated favorites ids list with no more {anime_id}")
        return ('',204)

    return ('',204)

##--DELETE TOWATCH ROUTE--##
@app.route("/users/<username>/towatch/delete", methods=["GET", "POST"])
def delete_to_watch(username):
    if "username" not in session:
        raise Unauthorized

    if request.method == "POST":
        towatch_id = request.json['id']
        anime_title = request.json['title']

        print(f"{anime_title} is the name of the anime to be deleted")
        print(f"{towatch_id} is the id of the anime in the database to be deleted")
        anime_id = get_anime_id(anime_title)

        anime_entry = ToWatch.query.get(towatch_id)
        
        towatch_ids = get_anime_ids_db("towatch", username)

        print(f"This is the content of {towatch_ids} before removing {anime_id}")
        
        db.session.delete(anime_entry)
        db.session.commit()
        
        print(f"{towatch_ids} should be the new latest updated favorites ids list with no more {anime_id}")

        return ('',204)

    return ('',204)

#--DELETE USER--##
@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):

     if request.method == "POST":
        user = User.query.get(username)
        session.pop("username")
        db.session.delete(user)
        db.session.commit()
        return redirect("/")
