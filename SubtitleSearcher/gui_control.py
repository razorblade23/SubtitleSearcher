

def language_selector(values):
    language_selected = []
    try:
        if values['LangENG']:
            language_selected.append('eng')
        elif values['LangCRO']:
            language_selected.append('hrv')
        elif values['LangSRB']:
            language_selected.append('srb')
        elif values['LangBOS']:
            language_selected.append('bos')
    except TypeError:
        language_selected.append('eng')
    return language_selected

def search_by_single_file(values, lang):
    from SubtitleSearcher.data import openSubtitles, movies
    from SubtitleSearcher.main import sg
    import urllib
    opensubs = openSubtitles.searchOpenSubtitles()
    try:
        hashed_file = opensubs.hashFile(values['SINGLEFILE'])
        fileSize = opensubs.sizeOfFile(values['SINGLEFILE'])
    except FileNotFoundError:
        sg.popup_ok('File not found, please try again', title='File not found')
    else:
        movie = movies.Movie(fileSize, hashed_file)
        link = opensubs.create_link(bytesize=fileSize, hash=hashed_file, language=lang)
        subtitles = opensubs.request_subtitles(link)
    #subtitles=[] # Comment / Uncomment this to simulate finding hash failed
    all_subs = []
    if len(subtitles) == 0: # If finding movie with hash failed and list "subtitles" is empty so it length is 0 
        movie_name = sg.popup_get_text('Finding subtitles using hash failed!\nPlease input name of your movie.')
        if movie_name != None:
            movie_name.lower() # Make all letters of movie name lowercase
            movie_name = urllib.parse.quote(movie_name) # Make words URL friendly
            link = opensubs.create_link(query=movie_name, language=lang) # Create a link to search for movie by its name and language
        try:
            subtitles = opensubs.request_subtitles(link)
            for number, subtitle in enumerate(subtitles):
                if number == 0:
                    movie.set_metadata(subtitle['MovieName'], subtitle['MovieYear'], subtitle['SubDownloadLink'], subtitle['ZipDownloadLink'], subtitle['IDMovieImdb'])
                number = movies.MovieSubtitle(subtitle['SubFileName'], subtitle['SubLanguageID'], subtitle['SubFormat'], subtitle['SubDownloadsCnt'], subtitle['SubDownloadLink'], subtitle['ZipDownloadLink'], subtitle['Score'])
                all_subs.append(number)
        except:
            sg.popup_ok('We got error 503.\nThat usually means there is maintanance\n under way on open subtitles servers.\nPlease try another method for serching or try again later',
                        title='Error', )
    else:
        for number, subtitle in enumerate(subtitles):
            if number == 0:
                movie.set_metadata(subtitle['MovieName'], subtitle['MovieYear'], subtitle['SubDownloadLink'], subtitle['ZipDownloadLink'], subtitle['IDMovieImdb'])
            number = movies.MovieSubtitle(subtitle['SubFileName'], subtitle['SubLanguageID'], subtitle['SubFormat'], subtitle['SubDownloadsCnt'], subtitle['SubDownloadLink'], subtitle['ZipDownloadLink'], subtitle['Score'])
            all_subs.append(number)
    return movie, all_subs
