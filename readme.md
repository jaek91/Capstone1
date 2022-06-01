# Capstone Project 1 (Anime Database and Recommender) Proposal

## Goals
This anime database website will allow for users to search for anime by specifying various filters such as year released, genres, completed, and so forth. 

It will allow for users to make lists of anime that they have watched or plan on watching. It will also suggest various anime and provide recommendations based on what the user has searched or favorited.

## User demographics
People who enjoy watching anime and want to track their viewing online as well as wanting to search for new anime to watch.

## Data being used
I will be using JSON data providing information about each anime using Kitsu API (https://kitsu.docs.apiary.io/#). Additionally, I would like the data retrieved to contain information on a per anime basis based on what the user can search for such as year released, genre, score received on MAL and so forth.

## Database Schema
[Schema Draft](https://app.quickdatabasediagrams.com/#/d/TO3e7P)
- **User** -- One user can have many lists of anime favorites which are separated by list names
- **Watched list** -- consists of the list of animes that user tracks as having completed
- **To-Watch list** -- consists of the list of animes that user tracks as to be watched
- **Favorites** -- consists of custom lists of anime that the user has favorited. User can create no more than 10 of these customized lists

## Potential issues
1. All MyAnimeList data provided on the Jikan API is cached on servers for 24 hours so it is possible for the information to not be most up to date when the user makes the request
2. Difficulty of implementing an accurate recommendation system given the data I have to work with

## Sensitive Information to Secure
Mainly user sensitive information such as passwords and emails.
Passwords will be secured via Bcrypt and username along with associated user information will be stored in the database.

## Functionality of the app
- User will be able to create a profile with about me and other descriptions
- User will be able to create lists categorized by type (watched, to watch and favorites)
- User can search for new anime on the database
- User will be recommended anime based on what their favorites list or on the home page based on their search history

## User flow
- User logs on which will display their profile -> access their about me, and links to their various anime lists
- On homepage, user can search for anime and specify filters using various dropdowns which will be preconfigured
- On the homepage, user will be recommended anime based on either what they’ve recently searched or based on their favorites list 

## Stretch Goals (Beyond CRUD)
1. User can see graphs visually displaying their anime lists separated by scores, genres, etc.
2. Users can leave comments on another users profile (social aspect)

