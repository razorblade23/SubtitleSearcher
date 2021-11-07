import ntpath
from SubtitleSearcher.data import imdb_metadata
from SubtitleSearcher.main import sg

def intro_dialog():
    dialog = sg.popup_ok('''
    This app is still in early alpha. 
    Current version is 0.0.2-alpha.

                        Not all features are developed.

    Currently working:
        * Searching using single video file

        * Language chooser

        * Searching by file hash first.
            If that fails, then it searches by filename.

        * First result is probably the best 
            for your specific movie

    Features to work on:
        -> Quick mode - selects first subtitle in list 
            automaticly and dowloads it next to file 
            with matching filename.

        -> Download and make local copy of IMDB database 
            so it can work faster

        -> Implementing more languages to choose from

        -> Ability to select multiple languages 
            (requires multiple querys to server)

        -> Ability to select multiple sources 
            for subtitles search 
            (openSubtitles is only one for now)
                ''', title='SubbyDoo v.0.0.2-alpha INFO', text_color='white')
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

def search_by_single_file(values, lang, window):
    from SubtitleSearcher.data import openSubtitles, movies
    import urllib
    opensubs = openSubtitles.searchOpenSubtitles()
    sg.popup_notify('Searching subtitles, please wait', title='Search started', display_duration_in_ms=1200, fade_in_duration=100)
    try:
        hashed_file = opensubs.hashFile(values['SINGLEFILE'])
        fileSize = opensubs.sizeOfFile(values['SINGLEFILE'])
    except FileNotFoundError:
        sg.popup_ok('File not found, please try again', title='File not found')
    else:
        movie = movies.Movie(fileSize, hashed_file, values['SINGLEFILE'], ntpath.basename(values['SINGLEFILE']))
        movie.set_from_filename()
        #print(f'\nMetadata extracted from filename:\n{movie.movie_info}')
        metadata = imdb_metadata.search_imdb_by_title(movie.title)
        type_of_video = metadata[0]['kind']
        movie.set_movie_kind(type_of_video)
        movie_imdb_id = metadata[0].movieID
        movie.set_imdb_id(movie_imdb_id)
        window['STATUSBAR'].update(f'Movie name: {movie.title} - IMDB ID: {movie.imdb_id}')
        link = opensubs.create_link(imdb=movie.imdb_id, bytesize=fileSize, hash=hashed_file, language=lang)
        subtitles = opensubs.request_subtitles(link)
    #subtitles=[] # Comment / Uncomment this to simulate finding hash failed
    all_subs = []
    if len(subtitles) == 0: # If finding movie with hash failed and list "subtitles" is empty so it length is 0
        movie_name = movie.title
        if movie_name != None:
            movie_name.lower() # Make all letters of movie name lowercase
            movie_name = urllib.parse.quote(movie_name) # Make words URL friendly
            link = opensubs.create_link(query=f'{movie_name} {movie.excess} {movie.extended}', language=lang) # Create a link to search for movie by its name and language
        try:
            subtitles = opensubs.request_subtitles(link)
            for number, subtitle in enumerate(subtitles):
                #print(f'\nSubtitle metadata extracted from subtitle:\n{subtitle}')
                number = movies.Subtitle(subtitle)
                all_subs.append(number)
        except:
            sg.popup_ok('We got error 503.\nThat usually means there is maintanance\n under way on open subtitles servers.\nPlease try another method for serching or try again later',
                        title='Error', )
    else:
        for number, subtitle in enumerate(subtitles):
            #print(f'\nSubtitle metadata extracted from subtitle:\n{subtitle}')
            number = movies.Subtitle(subtitle)
            all_subs.append(number)
    return movie, all_subs
