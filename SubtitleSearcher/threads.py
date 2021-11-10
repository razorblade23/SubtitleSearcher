from threading import ThreadError
from SubtitleSearcher.main import threading
from SubtitleSearcher.data import imdb_metadata
from SubtitleSearcher.data import openSubtitles, movies
import ntpath
import queue
import time

opensubs = openSubtitles.searchOpenSubtitles()
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

def SearchForSubtitles(link):
    subtitles = opensubs.request_subtitles(link)
    return subtitles

def search_by_multy_file(OpenSubtitlesSearchAlg, file_path, language, count):
    print(f'Starting thread: {count}')
    try:
        hashed_file = opensubs.hashFile(file_path)
        fileSize = opensubs.sizeOfFile(file_path)
    except FileNotFoundError:
        print('File not found, please try again')
        FileSearcherLock.release()
    else:
        movie = movies.Movie(fileSize, hashed_file, file_path, ntpath.basename(file_path))
        FileSearcherLock.acquire()
        movie.set_from_filename()
        FileSearcherLock.release()
        #print(f'\nMetadata extracted from filename:\n{movie.movie_info}')
        metadata = imdb_metadata.search_imdb_by_title(movie.title)
        #metadata = imdb_metadata.search_imdb_by_title(movie.title)
        #print(metadata)
        type_of_video = metadata[0]['kind']
        movie.set_movie_kind(type_of_video)
        movie_imdb_id = metadata[0].movieID
        movie.set_imdb_id(movie_imdb_id)
        #movie = movie_setup(fileSize, hashed_file, values, file_path)
        search_alg = OpenSubtitlesSearchAlg(movie, language)
        subtitles, all_subs = search_alg.subtitleSearchStep1()
        #subtitles = []
        if len(subtitles) == 0:
            subtitles, all_subs = search_alg.subtitleSearchStep2()
            if len(subtitles) == 0:
                subtitles, all_subs = search_alg.subtitleSearchStep3()
        #subtitles=[] # Comment / Uncomment this to simulate finding hash failed
        
    first_sub = all_subs[0]
    subsQueve.put(first_sub)
    print(f'''
    Job done - {movie.title}
    Episode: {movie.episode} Season: {movie.season}
    Video filename: {movie.file_name}
    Subtitle filename: {first_sub.SubFileName}
    Thread {count}
    ''')
    
