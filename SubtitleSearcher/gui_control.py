import ntpath
from SubtitleSearcher import threads
from SubtitleSearcher.data import imdb_metadata
from SubtitleSearcher.main import sg
from SubtitleSearcher.data import openSubtitles, movies, titlovi_com
from SubtitleSearcher.threads import SearchForSubtitles, movieQueve, subsQueve

import urllib
import threading
import queue



movieQueve = queue.Queue()
allSubsQueve = queue.Queue()

opensubs = openSubtitles.searchOpenSubtitles()

def intro_dialog():
    dialog = sg.popup_ok('''
    This app is still in early alpha. 
    Current version is 0.0.2-alpha.

                        Not all features are developed.

    Currently working:
        * Searching using single video file

        * Searching using multiple video files
            (Quick mode only !)

        * Implementing multi-threaded operations 
            for smooth experience

        * Language chooser

        * Quick mode - selects first subtitle in list 
            automaticly and downloads it next to file 
            with matching filename.

    Features to work on:
        -> Implementing TV series search
        
        -> Implementing of system tray or widget
            option for quick access

        -> Download and make local copy of IMDB database 
            so it can work faster

        -> Implementing more languages to choose from

        -> Ability to select multiple languages 
            (requires multiple querys to server)

        -> Ability to select multiple sources 
            for subtitles search 
            (openSubtitles is only one for now)
                ''', title='SubbyDoo v.0.0.2-alpha INFO', text_color='white', font='Any 12')
    return dialog

class OpenSubtitlesSearchAlg:
    def __init__(self, movie, language):
        self.movie = movie
        self.all_subs = []
        self.language = language
        #print(f'Video title: {movie.title}')

    def subtitleSearchStep1(self):
        print('Step 1 - search by file hash')
        link = opensubs.create_link(imdb=self.movie.imdb_id, bytesize=self.movie.byte_size, hash=self.movie.file_hash, language=self.language)
        #print(f'Link for step 1:\n{link}')
        subtitles = SearchForSubtitles(link)
        #subtitles = opensubs.request_subtitles(link)
        for number, subtitle in enumerate(subtitles):
            #print(f'\nSubtitle metadata extracted from subtitle:\n{subtitle}')
            number = movies.openSubtitlesSub(subtitle)
            self.all_subs.append(number)
        if len(self.all_subs) == 0:
            print('Step 1 failed')
        else:
            print('Step 1 success\n')
        return subtitles, self.all_subs

    def subtitleSearchStep2(self):
        print('Step 2 - Searching by filename')
        if self.movie.title != None:
            self.movie.title.lower() # Make all letters of movie name lowercase
            query = openSubtitles.searchOpenSubtitles.make_search_string(title=self.movie.title, episode=self.movie.episode, season=self.movie.season, year=self.movie.year, quality=self.movie.quality, resolution=self.movie.resolution, encoder=self.movie.encoder, excess=self.movie.excess)
            link = opensubs.create_link(query=query, language=self.language) # Create a link to search for movie by its name and language
            link = urllib.parse.quote(link, safe=':/')
            #print(f'Link for step 2:\n{link}')
        try:
            subtitles = SearchForSubtitles(link)
            #subtitles = opensubs.request_subtitles(link2)
            #print(f'\n{subtitles}\n')
        except:
            sg.popup_ok('We got error 503.\nThat usually means there is maintanance\n under way on open subtitles servers.\nPlease try another method for serching or try again later',
                        title='Error')
        else:
            for number, subtitle in enumerate(subtitles):
                #print(f'\nSubtitle metadata extracted from subtitle:\n{subtitle}')
                number = movies.openSubtitlesSub(subtitle)
                self.all_subs.append(number)

        if len(subtitles) == 0:
            print('Step 2 failed')
        else:
            print('Step 2 success\n')
        return subtitles, self.all_subs

    def subtitleSearchStep3(self):
        print('Step 3 - Searching by IMDB ID and filename')
        if self.movie.title != None:
            self.movie.title.lower() # Make all letters of movie name lowercase
            query = openSubtitles.searchOpenSubtitles.make_search_string(title=self.movie.title, episode=self.movie.episode, season=self.movie.season, year=self.movie.year, quality=self.movie.quality, resolution=self.movie.resolution, encoder=self.movie.encoder, excess=self.movie.excess)
            link = opensubs.create_link(imdb=self.movie.imdb_id, query=query, language=self.language) # Create a link to search for movie by its name and language
            link = urllib.parse.quote(link, safe=':/')
            #print(f'Link for step 3:\n{link}')
        try:
            subtitles = SearchForSubtitles(link)
            #subtitles = opensubs.request_subtitles(link2)
            #print(f'\n{subtitles}\n')
        except:
            sg.popup_ok('We got error 503.\nThat usually means there is maintanance\n under way on open subtitles servers.\nPlease try another method for serching or try again later',
                        title='Error')
        else:
            for number, subtitle in enumerate(subtitles):
                #print(f'\nSubtitle metadata extracted from subtitle:\n{subtitle}')
                number = movies.openSubtitlesSub(subtitle)
                self.all_subs.append(number)

        if len(subtitles) == 0:
            print('Step 3 failed')
        else:
            print('Step 3 success\n')
        return subtitles, self.all_subs




def StatusBarMainUpdate(window, update):
    return window['STATUSBAR'].update(update)
def StatusBarVersionUpdate(window, update):
    return window['STATUSBAR1'].update(update)

def language_selector(values):
    language_selected = []
    try:
        if values['LangENG']:
            language_selected.append('eng')
        elif values['LangCRO']:
            language_selected.append('hrv')
        elif values['LangSRB']:
            language_selected.append('scc')
        elif values['LangBOS']:
            language_selected.append('bos')
        elif values['LangSLO']:
            language_selected.append('slv')
    except TypeError:
        language_selected.append('eng')
    return language_selected

def movie_setup(file_size, file_hash, file_path):
    movie = movies.Movie(file_size, file_hash, file_path, ntpath.basename(file_path))
    movie.set_from_filename()
    #print(f'\nMetadata extracted from filename:\n{movie.movie_info}')
    metadata = imdb_metadata.search_imdb_by_title(movie.title)
    #metadata = imdb_metadata.search_imdb_by_title(movie.title)
    #print(metadata)
    type_of_video = metadata[0]['kind']
    movie.set_movie_kind(type_of_video)
    movie_imdb_id = metadata[0].movieID
    movie.set_imdb_id(movie_imdb_id)
    return movie

def select_engine(values):
    engines = []
    if values['USEOPEN'] and values['USETITLOVI']:
        engines = ['OpenSubtitles', 'Titlovi.com']
    elif values['USEOPEN']:
        engines = ['OpenSubtitles']
    elif values['USETITLOVI']:
        engines = ['Titlovi.com']
    return engines


def define_movie(file_path):
    try:
        hashed_file = opensubs.hashFile(file_path)
        fileSize = opensubs.sizeOfFile(file_path)
    except FileNotFoundError:
        sg.popup_ok('File not found, please try again', title='File not found')
    else:
        movie = movie_setup(fileSize, hashed_file, file_path)
    return movie

def search_opensubs(language, movie):
    open_subs = []
    print('Running OpenSubtitles search')
    search_alg = OpenSubtitlesSearchAlg(movie, language)
    subtitles, subs_objects = search_alg.subtitleSearchStep1()
    if len(subtitles) == 0:
        subtitles, subs_objects = search_alg.subtitleSearchStep2()
        if len(subtitles) == 0:
            subtitles, subs_objects = search_alg.subtitleSearchStep3()
    for sub in subs_objects:
        open_subs.append(sub)
    return open_subs

def search_titlovi(language, movie, user_object):
    titlovi_subs = []
    print('Running Titlovi.com search')
    user_object.search_by_filename(movie.title, movie.year)
    user_object.set_language(language)
    user_object.search_API()
    for number, subtitle in enumerate(user_object.subtitles):
        number = movies.titloviComSub(subtitle)
        titlovi_subs.append(number)
    return titlovi_subs

def search_by_multy_file(values, file_path, language, window):
    try:
        hashed_file = opensubs.hashFile(file_path)
        fileSize = opensubs.sizeOfFile(file_path)
    except FileNotFoundError:
        sg.popup_ok('File not found, please try again', title='File not found')
    else:
        movie = movie_setup(fileSize, hashed_file, values, file_path)
        window['STATUSBAR'].update(f'Movie name: {movie.title} - IMDB ID: {movie.imdb_id}')
        search_alg = OpenSubtitlesSearchAlg(movie, language)
        subtitles, all_subs = search_alg.subtitleSearchStep1()
        if len(subtitles) == 0:
            subtitles, all_subs = search_alg.subtitleSearchStep2()
            if len(subtitles) == 0:
                subtitles, all_subs = search_alg.subtitleSearchStep3()
        #subtitles=[] # Comment / Uncomment this to simulate finding hash failed
    return movie, all_subs
