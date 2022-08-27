import requests
from models import User, Favorites, Watched, ToWatch

def get_search_results(title, num=0):
    """ Main function to display anime search results from making API calls"""
    r = requests.get('https://kitsu.io/api/edge/anime/?include=categories', params={"filter[text]": title, "page[limit]": 5})
    response = r.json()

    results = []
    for i in range(3):
        data = response['data'][i]
        id = data['id']

        anime_title = data['attributes']['canonicalTitle']
        synopsis = data['attributes']['synopsis']
        img_url = data['attributes']['posterImage']['medium']
        
        # categories = data['relationships']['categories']['data']
        # category_ids = [d['id'] for d in categories]
        # categories_names = return_categories(category_ids)

        result = {"id": id , "title": anime_title, "synopsis": synopsis, "img_url": img_url, 
                 "num": num}  ## "Favorites", "ToWatch", "Watched" are booleans on whether the anime is in a certain list
        results.append(result)
        num = num + 1
        # f"Favorites-{num}": False, f"ToWatch-{num}": False, f"Watched-{num}": False,
    return results

def get_anime(id):
    """Helper function to get anime data in JSON based on the anime id provided"""
    r = requests.get('https://kitsu.io/api/edge/anime', params={"filter[id]": id, "page[limit]": 5})
    response = r.json()

    data = response['data'][0]
    title = data['attributes']['canonicalTitle']
    synopsis = data['attributes']['synopsis']
    img_url = data['attributes']['posterImage']['medium']
    result = {"title": title, "synopsis": synopsis, "img_url": img_url, "id": id}
   
    return result

def get_anime_id(title):
     """Helper function to get the anime id based on the English title provided"""
     r = requests.get('https://kitsu.io/api/edge/anime', params={"filter[text]": title, "page[limit]": 5})
     response = r.json()
     anime_id = response['data'][0]['id']

     return anime_id

def get_anime_ids_db(category, username):
    """Helper function to retrieve current ids as stored in the database by anime list category"""
    if category == "favorites":
       
        fav_titles = Favorites.query.with_entities(Favorites.name).filter_by(username = username).all()
        curr_db_fav_titles = [name[0] for name in fav_titles]
        fav_anime_ids = [get_anime_id(title) for title in curr_db_fav_titles]
        return fav_anime_ids

    elif category == "watched":
        
        watched_titles = Watched.query.with_entities(Watched.name).filter_by(username = username).all()
        curr_db_watched_titles = [name[0] for name in watched_titles]  
        watched_anime_ids = [get_anime_id(title) for title in curr_db_watched_titles]

        return watched_anime_ids

    else:
        towatch_titles = ToWatch.query.with_entities(ToWatch.name).filter_by(username = username).all()
        curr_db_towatch_titles = [name[0] for name in towatch_titles]  
        towatch_anime_ids = [get_anime_id(title) for title in curr_db_towatch_titles]

        return towatch_anime_ids

def convert_title_to_jp(title):
    """An helper function to convert the English anime name to the JP name because the 
    database we're comparing user searched entries to only has JP names"""

    r = requests.get('https://kitsu.io/api/edge/anime', params={"filter[text]": title, "page[limit]": 5})
    response = r.json()
    
    data = response['data'][0]
    jp_title = data['attributes']['titles']['en_jp']

    return jp_title

def get_unique_titles(res, title):
    """Helper function to retain only the unique elements in the context of providing recommendations so we don't 
    recommend the same anime from one of the ones randomly picked from the favorites list as one of their favorites
    """
    
    titles = []

    for entry in res["name"].values():
        if entry != title:
            titles.append(entry)
    return titles

def get_info_recommended_titles(lst):
    """Helper function to provide the crucial anime information for the recommended titles to display 
    on user page under recommendations"""
    
    results = []
    
    for anime_title in lst:
        r = requests.get('https://kitsu.io/api/edge/anime/?include=categories', params={"filter[text]": anime_title, "page[limit]": 5})
        response = r.json()
        
        data = response['data'][0]
        id = data['id']

        anime_title = data['attributes']['canonicalTitle']
        img_url = data['attributes']['posterImage']['small']
        
        result = {"id": id , "title": anime_title, "img_url": img_url}
        results.append(result)
        
    return results

def check_anime_in_db_lists(anime_results, username):
    """This method checks whether if the entries from anime_results (JSON of anime data) which are from a user's search
    are in the database for the various lists (i.e. Favorites, To-Watch, Watched) or if they're not. 
    If they are already in the database, set the values to true """

    fav_titles = Favorites.query.with_entities(Favorites.name).filter_by(username = username).all()
    db_fav_titles = [name[0] for name in fav_titles]
    towatch_titles = ToWatch.query.with_entities(ToWatch.name).filter_by(username = username).all()
    db_towatch_titles = [name[0] for name in towatch_titles]
    watched_titles = Watched.query.with_entities(Watched.name).filter_by(username = username).all()
    db_watched_titles = [name[0] for name in watched_titles]
    
    for dict in anime_results:  
        currTitle = dict["title"]
        curr_entry_num = dict["num"]

        if currTitle in db_fav_titles and currTitle in db_watched_titles:
            dict[f"Favorites-{curr_entry_num}"] = "true"
            dict[f"Watched-{curr_entry_num}"] = "true" 
            continue
        elif currTitle in db_fav_titles:
            dict[f"Favorites-{curr_entry_num}"] = "true"
            continue
        elif currTitle in db_watched_titles:
            dict[f"Watched-{curr_entry_num}"] = "true"   
            continue    
        elif currTitle in db_towatch_titles:
            dict[f"ToWatch-{curr_entry_num}"] = "true"
            continue
        else:
            dict[f"Favorites-{curr_entry_num}"] = "false"
            dict[f"ToWatch-{curr_entry_num}"] = "false"
            dict[f"Watched-{curr_entry_num}"] = "false"
        
    return