# IADB Project (Internet Anime Database)

## Purpose
This IADB web application will allow for users to search for anime by specifying various filters such as year released, genres, completed, and so forth. 

It will also allow for users to categorize anime that they have watched or plan on watching into various lists (favorites, watched and to-watch). It will also suggest various anime and provide recommendations based on what the user has searched or favorited.

## Deployed at
[IADB App](https://iadb-app.herokuapp.com/)

## User demographics
People who enjoy watching anime and want to track their viewing online as well as wanting to search for new anime to watch.

## API being used
I am using JSON data providing information about each anime retrieved via the Kitsu API (https://kitsu.docs.apiary.io/#). I chose this API because it's minimalistic, straightforward to use and has a lot of features to search for per route

## Technology stack used
- *Backend*: Python, Flask, PostgresSQL, Pandas
- *Frontend*: Javascript, HTML, CSS, Bootstrap

## Functionality of the app
- User will be able to create a profile with an about me section
- User can search for new anime on the database
- Authenticated Users (i.e. those who are logged in) will be able to categorize searched animes into various lists (watched, to watch and favorites)
- Authenticated Users (i.e. those who are logged in) will be recommended anime based on what their favorites list or on the home page based on their search history. I wanted to implement this because I was interested in recommendation engines and how we use Machine Learning algorithms to do so.

## User flow
- User logs on which will display their profile -> access their about me, and links to their various anime lists
- On homepage, user can search for anime and specify filters using various dropdowns which will be preconfigured
- On the homepage, user will be recommended anime based on either what they’ve recently searched or based on their favorites list 

