import ntpath
from SubtitleSearcher import threads
from SubtitleSearcher.data import imdb_metadata
from SubtitleSearcher.main import sg
from SubtitleSearcher.data import openSubtitles, movies
from SubtitleSearcher.threads import ImdbSearchByTitle, SearchForSubtitles, movieQueve, subsQueve
import urllib
import threading

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

        * Language chooser

        * Quick mode - selects first subtitle in list 
            automaticly and downloads it next to file 
            with matching filename.

    Features to work on:
        -> Implementing TV series search

        -> Implementing multi-threaded operations 
            for smooth experience
        
        -> Implementing of system tray 
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
            language_selected.append('srp')
        elif values['LangBOS']:
            language_selected.append('bos')
        elif values['LangSLO']:
            language_selected.append('slv')
    except TypeError:
        language_selected.append('eng')
    return language_selected

def movie_setup(file_size, file_hash, values, file_path):
    movie = movies.Movie(file_size, file_hash, file_path, ntpath.basename(file_path))
    movie.set_from_filename()
    #print(f'\nMetadata extracted from filename:\n{movie.movie_info}')
    MovieMetadataThread = threading.Thread(target=ImdbSearchByTitle, args=[movie])
    MovieMetadataThread.start()
    metadata = movieQueve.get()
    MovieMetadataThread.join()
    #metadata = imdb_metadata.search_imdb_by_title(movie.title)
    #print(metadata)
    type_of_video = metadata[0]['kind']
    movie.set_movie_kind(type_of_video)
    movie_imdb_id = metadata[0].movieID
    movie.set_imdb_id(movie_imdb_id)
    return movie

def subtitle_search(movie, language, hash):
    print(f'\nMovie name: {movie.title}')
    all_subs = []
    if hash == True:
        print('Step 1 - Searching by movie hash')
        link = opensubs.create_link(imdb=movie.imdb_id, bytesize=movie.byte_size, hash=movie.file_hash, language=language)
        #print(f'Link for step 1:\n{link}')
        subThread = threading.Thread(target=SearchForSubtitles, args=[link])
        subThread.start()
        subtitles = subsQueve.get()
        subThread.join()
        #subtitles = opensubs.request_subtitles(link)
        for number, subtitle in enumerate(subtitles):
            #print(f'\nSubtitle metadata extracted from subtitle:\n{subtitle}')
            number = movies.Subtitle(subtitle)
            all_subs.append(number)
        if len(all_subs) == 0:
            print('Step 1 failed\n')
        else:
            print('Step 1 success\n')
    else:
        print('Step 2 - Searching by filename')
        if movie.title != None:
            movie.title.lower() # Make all letters of movie name lowercase
            query = openSubtitles.searchOpenSubtitles.make_search_string(title=movie.title, year=movie.year, quality=movie.quality, resolution=movie.resolution, encoder=movie.encoder, excess=movie.excess)
            link2 = opensubs.create_link(imdb=movie.imdb_id, query=query, language=language) # Create a link to search for movie by its name and language
            link2 = urllib.parse.quote(link2, safe=':/')
            print(f'Link for step 2:\n{link2}')
        try:
            subThread = threading.Thread(target=SearchForSubtitles, args=[link2])
            subThread.start()
            subtitles = subsQueve.get()
            subThread.join()
            #subtitles = opensubs.request_subtitles(link2)
            #print(f'\n{subtitles}\n')
        except:
            sg.popup_ok('We got error 503.\nThat usually means there is maintanance\n under way on open subtitles servers.\nPlease try another method for serching or try again later',
                        title='Error')
        else:
            for number, subtitle in enumerate(subtitles):
                #print(f'\nSubtitle metadata extracted from subtitle:\n{subtitle}')
                number = movies.Subtitle(subtitle)
                all_subs.append(number)

        if len(subtitles) == 0:
            print('Step 2 failed\n')
        else:
            print('Step 2 success\n')
    return subtitles, all_subs

def search_by_single_file(values, language, window):
    try:
        hashed_file = opensubs.hashFile(values['SINGLEFILE'])
        fileSize = opensubs.sizeOfFile(values['SINGLEFILE'])
    except FileNotFoundError:
        sg.popup_ok('File not found, please try again', title='File not found')
    else:
        movie = movie_setup(fileSize, hashed_file, values, values['SINGLEFILE'])
        window['STATUSBAR'].update(f'Movie name: {movie.title} - IMDB ID: {movie.imdb_id}')
        subtitles, all_subs = subtitle_search(movie, language, hash=True)
        #subtitles=[] # Comment / Uncomment this to simulate finding hash failed
        if len(subtitles) == 0:
            subtitles, all_subs = subtitle_search(movie, language, hash=False)
    return movie, all_subs

def search_by_multy_file(values, file_path, language, window):
    try:
        hashed_file = opensubs.hashFile(file_path)
        fileSize = opensubs.sizeOfFile(file_path)
    except FileNotFoundError:
        sg.popup_ok('File not found, please try again', title='File not found')
    else:
        movie = movie_setup(fileSize, hashed_file, values, file_path)
        window['STATUSBAR'].update(f'Movie name: {movie.title} - IMDB ID: {movie.imdb_id}')
        subtitles, all_subs = subtitle_search(movie, language, hash=True)
        #subtitles=[] # Comment / Uncomment this to simulate finding hash failed
        if len(subtitles) == 0:
            subtitles, all_subs = subtitle_search(movie, language, hash=False)
    return movie, all_subs
