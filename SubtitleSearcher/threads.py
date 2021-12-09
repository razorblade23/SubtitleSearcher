from threading import ThreadError
from SubtitleSearcher.main import threading, log
from SubtitleSearcher.data.opeSubtitle_new import SearchForSubs
import urllib
import queue
import requests
import json
from imdb import IMDb
import asyncio
IMDB = IMDb()



FileHandlerLock = threading.Lock()
FileSearcherLock = threading.Lock()
movieQueve = queue.Queue()
subsQueve = queue.Queue()

def ZipDownloaderThreaded(zip_handler, thread_nmb='1'):
    FileHandlerLock.acquire()
    file_download = zip_handler.download_zip()
    if file_download:
        print(f'Thread {thread_nmb} working with\n{zip_handler.filename}')
        print(f'Subtitle downloaded - thread {thread_nmb}')
        try:
            print(f'Extracting from ZIP - thread {thread_nmb}')
            zip_handler.extract_zip()
        except FileNotFoundError:
            print(f'Bad zip downloaded - thread {thread_nmb}')
            FileHandlerLock.release()
        else:
            try:
                print(f'Moving files to target directory - thread {thread_nmb}')
                zip_handler.move_files()
            except FileNotFoundError:
                print(f'Cant move file - thread {thread_nmb}')
                FileHandlerLock.release()
            else:
                print(f'Job done, releasing lock - thread {thread_nmb}\n')
                FileHandlerLock.release()

def findVideoDetails_threaded(title, queve_in):
    log.info(f'Searching IMDB details by: {title}')
    search = IMDB.search_movie(title)
    queve_in.put(search)

def searchOpenSubtitles_threaded(payload, queve_in):
    API_KEY = 'CIVqd03XEgIT4ERQX0AGlUjcaFCfRdyI'
    BASE_URL = 'https://api.opensubtitles.com/api/v1/'
    #search = SearchForSubs()
    '''Search for subtitles based on payload
    param: payload - parameters for searchin subtitle like movie name, IMDB ID, etc...'''

    log.debug(f'Searching OpenSubtitles using payload: {payload}')
    url = f'{BASE_URL}subtitles'
    headers = {
        'Content-Type': "application/json",
        'Api-Key': API_KEY
    }
    url_string = urllib.parse.urlencode(payload, safe=',')
    replaced = url_string.replace('+', ' ')
    response = requests.get(url, headers=headers, params=replaced, allow_redirects=True)
    json_dict = json.loads(response.text)
    data = json_dict['data']
    for subtitle in data:
        queve_in.put(subtitle)

def searchTitlovi_threded():
    pass


