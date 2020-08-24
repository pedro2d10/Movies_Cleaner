import os
from os.path import isfile, join
import re

MOVIES_FOLDER = "/srv/dev-disk-by-label-volume1/Films/Films"

def parse_movie_title(movie):
    year = None
    if len(movie.split('.')) > 2:        
        for text in movie.split('.'):
            year = re.search('^(19|20)\d{2}$', text)
            if year is not None:
                break

    
    if year is not None:
        year = year.group(0)
    else:
        year = 1900

    return movie.split('.')[0], year



if os.path.exists(MOVIES_FOLDER):
    for file in os.listdir(MOVIES_FOLDER):
        if isfile(join(MOVIES_FOLDER, file)):
            name, year = parse_movie_title(file)
            print("Film : {} | Année : {}".format(name, year))
else:
    print("le répertoire {} n'existe pas, veuillez réessayer".format(MOVIES_FOLDER))