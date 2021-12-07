# Importing modules
import ntpath

import imdb
from SubtitleSearcher import threads
from SubtitleSearcher.data.imdb_metadata import search_imdb_by_title, ImdbID_queve
from SubtitleSearcher.main import sg
from SubtitleSearcher.threads import movieQueve, subsQueve
from SubtitleSearcher.data.movies import hashFile, sizeOfFile, Movie, titloviComSub

import urllib
import threading
import queue


# Sets queves to use with threads
movieQueve = queue.Queue()
allSubsQueve = queue.Queue()


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

# Update status bar helper function
def StatusBarUpdate(window, element_name, value=None, text_color=None, font=None, visible=None):
    return window[element_name].update(value=value, text_color=text_color, font=font, visible=visible)

# Get languges from GUI and set them in list
def language_selector(values):
    language_selected = []
    try:
        if values['LangENG']:
            language_selected.append('en')
        if values['LangCRO']:
            language_selected.append('hr')
        if values['LangSRB']:
            language_selected.append('sr')
        if values['LangBOS']:
            language_selected.append('bs')
        if values['LangSLO']:
            language_selected.append('sl')
    except TypeError:
        language_selected.append('en')
    return language_selected

# Set up engine select
def select_engine(values):
    engines = []
    if values['USEOPEN'] and values['USETITLOVI']:
        engines = ['OpenSubtitles', 'Titlovi.com']
    elif values['USEOPEN']:
        engines = ['OpenSubtitles']
    elif values['USETITLOVI']:
        engines = ['Titlovi.com']
    return engines

# Set up movie object
def define_movie(file_path):
    try:
        hashed_file = hashFile(file_path)
        fileSize = sizeOfFile(file_path)
    except FileNotFoundError:
        sg.popup_ok('File not found, please try again', title='File not found')
    else:
        movie = Movie(fileSize, hashed_file, file_path, ntpath.basename(file_path))
        movie.set_from_filename()
        findImdbId = threading.Thread(target=search_imdb_by_title, args=[movie.title], daemon=True)
        findImdbId.start()
    return movie

def setImdbIdFromThread(movie):
    metadata = ImdbID_queve.get()
    type_of_video = metadata[0]['kind']
    movie.set_movie_kind(type_of_video)
    movie_imdb_id = metadata[0].movieID
    movie.set_imdb_id(movie_imdb_id)

# Search titlovi.com
def search_titlovi(language, movie, user_object):
    titlovi_subs = []
    print('Running Titlovi.com search')
    if movie.episode != None or movie.season != None:
        if movie.episode != None:
            user_object.search_by_filename(movie.title, movie.year, episode=movie.episode)
        if movie.season != None:
            user_object.search_by_filename(movie.title, movie.year, season=movie.season)
    else:
        user_object.search_by_filename(movie.title, movie.year)
    user_object.set_language(language)
    user_object.search_API()
    for number, subtitle in enumerate(user_object.subtitles):
        number = titloviComSub(subtitle)
        titlovi_subs.append(number)
    return titlovi_subs

