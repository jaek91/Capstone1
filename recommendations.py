from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

## my collaborative filtering recommendation algorithm implementation is based off of what's mentioned on  
## https://www.kaggle.com/indralin/try-content-based-and-collaborative-filtering


anime_df = pd.read_csv("anime.csv")
my_stopword_list = ['and','to','the','of']

tfv = TfidfVectorizer(min_df=3,  max_features=None, 
            strip_accents='unicode', analyzer='word',token_pattern=r'\w{1,}',
            ngram_range=(1, 3),
            stop_words = my_stopword_list)

# Filling NaNs with empty string
anime_df['genre'] = anime_df['genre'].fillna('')
genres_str = anime_df['genre'].str.split(',').astype(str)

# we transform the data to get the tf-idf matrix 
tfidf_matrix = tfv.fit_transform(genres_str)

csm = cosine_similarity(tfidf_matrix, tfidf_matrix)

indices = pd.Series(anime_df.index, index = anime_df['name']).drop_duplicates()

def give_recommendations(title, csm = csm):
    """This function gives recommendations by title using the 
    Term Frequency (TF) and Inverse Document Frequency (IDF) method """

    # Get the index corresponding to the given title

    if title in indices:
       idx = indices[title]
    else:
        ## we can't provide recommendations if we can't find the anime in our database
        return False

    # Get an indexed version of pairwise similarity scores
    sim_scores = list(enumerate(csm[idx]))
    
    # Sort the animes by highest similarity scores
    sim_scores = sorted(sim_scores, key= lambda x: x[1], reverse=True)

    # Scores of the 5 most similar animes
    sim_scores = sim_scores[1:6]

    # Anime indices
    anime_indices = [i[0] for i in sim_scores]

    results = pd.DataFrame({'name': anime_df['name'].iloc[anime_indices].values})
    results_json = results.to_json(orient = 'columns')

    return results_json

