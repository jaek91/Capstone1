import requests 
import json

RECOMMENDATION_SERVICE_PATH = "https://recommendation-service.herokuapp.com/"

def give_recommendations(title):
    """this function will stay here"""
    parsed_title = title.replace(" ", ";")
    
    response = requests.get(f"{RECOMMENDATION_SERVICE_PATH}/recommendations/{parsed_title}")
    return response.json()