from SubtitleSearcher.main import threading
from SubtitleSearcher.data.imdb_metadata import search_imdb_by_title
from SubtitleSearcher.data import openSubtitles
import queue
import time

opensubs = openSubtitles.searchOpenSubtitles()
threadLock = threading.Lock()
movieQueve = queue.Queue()
subsQueve = queue.Queue()

def ZipDownloaderThreaded(zip_handler, thread_nmb='1'):
    file_download = zip_handler.download_zip()
    if file_download:
        print(f'Thread {thread_nmb} working with\n{zip_handler.filename}')
        print(f'Subtitle downloaded - thread {thread_nmb}')
        try:
            print(f'Extracting from ZIP - thread {thread_nmb}')
            print(f'Locking thread {thread_nmb}')
            threadLock.acquire()
            zip_handler.extract_zip()
        except FileNotFoundError:
            print(f'Bad zip downloaded - thread {thread_nmb}')
        else:
            try:
                print(f'Moving files to target directory - thread {thread_nmb}')
                zip_handler.move_files()
            except FileNotFoundError:
                print(f'Cant move file - thread {thread_nmb}')
            else:
                print(f'Job done, releasing lock - thread {thread_nmb}\n')
    threadLock.release()

def ImdbSearchByTitle(movie):
    print('\nThread movie search started')
    metadata = search_imdb_by_title(movie.title)
    movieQueve.put(metadata)

def SearchForSubtitles(link):
    subtitles = opensubs.request_subtitles(link)
    return subtitles
