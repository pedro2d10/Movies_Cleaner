import os
from os.path import isfile, join
import re
import requests

MOVIES_FOLDER = "/srv/dev-disk-by-label-volume1/Films/Films"

def parse_movie_title(movie):
    year = None
    movie_name = ""
    use_space = 1
    if len(movie.split(" ")) > len(movie.split('.')):
        movie_name_splited = movie.split(" ")
        movie_name_splited[len(movie_name_splited)-1]=movie_name_splited[len(movie_name_splited)-1].split('.')[0]
        use_space = 0
    else:
        movie_name_splited = movie.split('.')
    if len(movie_name_splited) > 2:        
        my_index=0
        for index, text in enumerate(movie_name_splited):
            text = ''.join(e for e in text if e.isalnum())
            year = re.search('^(19|20)\d{2}$', text)
            if year is not None:
                my_index = index
                break

        if year is None:
            movie_name = " ".join(movie_name_splited[:len(movie_name_splited) - use_space])
        else:
            #index = movie_name_splited.index(year.group(0))
            movie_name = " ".join(movie_name_splited[:my_index])


    if year is not None:
        year = year.group(0)
    else:
        year = 1900

    return movie_name, year

def get_imdb_movie(movie, year):
    url_base = "http://www.omdbapi.com/?apikey=dadf9e3a&t="
    if year != 1900 : 
        url = url_base + movie.replace(" ","+") + "&y=" + year
    else:
        url = url_base + movie.replace(" ", "+")
    imdb_movie = requests.get(url)
    imdb_json = imdb_movie.json()
    #if len(imdb_json) == 1:
    if imdb_json['Response'] != 'False':
        print("Film trouvé : {} | année :{}".format(imdb_json['Title'], imdb_json['Year']))


if os.path.exists(MOVIES_FOLDER):
    for file in os.listdir(MOVIES_FOLDER):
        if isfile(join(MOVIES_FOLDER, file)):
            name, year = parse_movie_title(file)
            print("Film : {} | Année : {}".format(name, year))
            if name != "":
                get_imdb_movie(name, year)
else:
    print("le répertoire {} n'existe pas, veuillez réessayer".format(MOVIES_FOLDER))