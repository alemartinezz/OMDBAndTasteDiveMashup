import requests_with_caching
import json


def get_movies_from_tastedive(movies):
    baseurl = "https://tastedive.com/api/similar"
    parameters = {}
    parameters["q"] = movies
    parameters["type"] = "movies"
    parameters["limit"] = 5
    tastedive_response = requests_with_caching.get(baseurl,
                                                   params=parameters)
    related_movies = json.loads(tastedive_response.text)
    return related_movies


def extract_movie_titles(related_movies):
    related_movie_names = [x["Name"] for x in
                           related_movies["Similar"]["Results"]]
    return related_movie_names


def get_related_titles(movie_names):
    related_movies_list = []

    for movie_name in movie_names:
        related_movies = get_movies_from_tastedive(movie_name)
        related_movie_names = extract_movie_titles(related_movies)

        related_movies_list = related_movies_list + [movie_name for movie_name in related_movie_names if related_movies_list.count(movie_name) == 0]

    return related_movies_list


def get_movie_data(title):
    baseurl = "http://www.omdbapi.com/"
    parameters = {}
    parameters["t"] = title
    parameters["r"] = "json"
    title_info_response = requests_with_caching.get(baseurl,
                                                   params=parameters)
    title_info = json.loads(title_info_response.text)
    return title_info


def get_movie_rating(title_info):
    rating = 0
    for ratings in title_info['Ratings']:
        if 'Rotten Tomatoes' in ratings.values():
            rating = int(ratings["Value"].replace('%', ''))
            return rating
    return rating


def get_sorted_recommendations(list_movie_titles):
    related_titles = get_related_titles(list_movie_titles)
    sorted_related_titles = sorted(related_titles, 
    key = lambda movie_name: (get_movie_rating(get_movie_data(movie_name)), movie_name), reverse=True)
    return sorted_related_titles
