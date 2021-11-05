from SubtitleSearcher.data.openSubtitles import requests
import json
from imdb import IMDb

IMDB = IMDb()


url = "https://imdb8.p.rapidapi.com/title/find"

def search_by_title(title):
    title_lower = str(title).lower()
    querystring = {"q":"{}".format(title_lower)}

    headers = {
        'x-rapidapi-host': "imdb8.p.rapidapi.com",
        'x-rapidapi-key': "9743ca3af2mshfadf70be77717d5p1925c1jsnd3aea8d44cd3"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    return response.text

def search_by_id(id_raw):
    id = 'tt{}'.format(id_raw)
    url = "https://imdb8.p.rapidapi.com/title/get-videos"

    querystring = {"tconst":"{}".format(id),"limit":"25","region":"US"}

    headers = {
        'x-rapidapi-host': "imdb8.p.rapidapi.com",
        'x-rapidapi-key': "9743ca3af2mshfadf70be77717d5p1925c1jsnd3aea8d44cd3"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    return json.loads(response.text)

def search_imdb_by_title(title):
    search = IMDB.search_movie(title)
    return search
