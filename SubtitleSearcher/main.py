# Importing modules
import logging
import logging.handlers
from contextlib import suppress
import os
def make_logger():
    with suppress(FileExistsError): os.mkdir('logs')
    LOG_FILENAME = 'logs/main.log'
    # Set up a specific logger with our desired output level
    log = logging.getLogger('MainLogger')
    log.setLevel(logging.DEBUG)
    handler = logging.handlers.RotatingFileHandler(
                LOG_FILENAME, maxBytes=100000, backupCount=2)
    log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(threadName)s - %(message)s')
    handler.setFormatter(log_format)
    handler.doRollover()
    log.addHandler(handler)
    return log
log = make_logger()
import json
import threading
import PySimpleGUI as sg
from tkinter.constants import E, FALSE
from SubtitleSearcher.engines import OpenSubtitles_API, Titlovi_API, ProccessOpenSubtitlesSubs, ProccessTitloviSubs, PersistanceManager
from SubtitleSearcher.data import handle_zip, starting_settings
from SubtitleSearcher.data.movies import GetFileHash, GetFileSize, Movie
from SubtitleSearcher import gui_control, gui_windows
import ntpath
import platform
import time

# Setting default paths for setting files in JSON format
SETTINGS_OSUBTITLES_PATH = 'SubtitleSearcher/data/user_settings/OpenSubtitles_settings.json'
SETTINGS_TITLOVI_PATH = 'SubtitleSearcher/data/user_settings/Titlovi_settings.json'
SETTINGS_USER_PATH = 'SubtitleSearcher/data/user_settings/User_settings.json'
log.info('Settings path set')

# Instantiating objects to use
openSubtitlesAPI = OpenSubtitles_API()
titloviAPI = Titlovi_API()
settingsManager = PersistanceManager()

# Set starting settings
def makeStartingSettings():
    settingsManager.save_userdata('OpenSubtitles', username='', password='')
    settingsManager.save_userdata('Titlovi', username='', password='')
    settingsManager.save_userdata('User', last_user_path='~/Downloads')

def loadFromSettings():
    SETTING_OPENSUBTITLES = settingsManager.load_userdata('OpenSubtitles')
    SETTING_TITLOVI = settingsManager.load_userdata('Titlovi')
    SETTING_USER = settingsManager.load_userdata('User')
    return SETTING_OPENSUBTITLES, SETTING_TITLOVI, SETTING_USER

# Set AutoLogin
def Autologin():
    SETTING_OPENSUBTITLES, SETTING_TITLOVI, SETTING_USER = loadFromSettings()
    if len(SETTING_OPENSUBTITLES['username']) > 0:
        openSubtitlesAPI.set_user(SETTING_OPENSUBTITLES['username'], SETTING_OPENSUBTITLES['password'])
        details = openSubtitlesAPI.login_user()
        openSubtitlesAPI.proccess_login_response(details)
    else:
        log.info('No user found in settings - OpenSubtitles')
    if len(SETTING_TITLOVI['username']) > 0:
        titloviAPI.set_user(SETTING_TITLOVI['username'], SETTING_TITLOVI['password'])
        details2 = titloviAPI.login_user()
        titloviAPI.proccess_login_response(details2)
    else:
        log.info('No user found in settings - Titlovi')

# Check for folders and files at start of program
def StartUp():
    '''
    Check for folders and files needed for startup.
    If there are none, make them
    '''
    os.makedirs('SubtitleSearcher/data/user_settings', exist_ok=True)
    if not os.path.isfile(SETTINGS_OSUBTITLES_PATH):
        log.info('No OpenSubtitles settings file, creating....')
        makeStartingSettings()

# Run StartUp function
StartUp()

# Thread AutoLogin scripts - as they are deamon threads there is no need to join them
log.info('Starting auto-login threads')
AutoLoginOpenS_thread = threading.Thread(target=Autologin, daemon=True, name='AutoLogin')
AutoLoginOpenS_thread.start()

# Check for system and use appropriate image for icon
system = platform.system()
if system == 'Windows':
    icon = 'images/image.ico'
if system == 'Linux':
    icon = 'images/image.png'
log.info(f'System detected: {system}')

main_layout = gui_windows.main_window()

# Display intro dialog
gui_control.intro_dialog()

def getVideoDetailsFromThread(movie, singleVideoQueve, movieDetailsThread):
    log.info('Getting video details from thread')
    try:
        movie_details = singleVideoQueve.get(timeout=2)
    except:
        log.critical('Movie details queve is empty')
    gui_control.setImdbIdFromThread(movie_details, movie)
    log.info(f'Movie set as: title - {movie.title}, kind - {movie.kind}')
    movieDetailsThread.join()
    return movie_details


# Get from JSON settings
def get_from_titlovi_settings():
    '''
    Get Titlovi.com settings
    '''
    with open(SETTINGS_TITLOVI_PATH, 'r') as json_obj:
        try:
            USERSETTINGS = json.load(json_obj)
        except json.decoder.JSONDecodeError:
            USERSETTINGSdict = {'username': '', 'password': ''}
            with open(SETTINGS_TITLOVI_PATH, 'w') as file:
                USERSETTINGS = json.dump(USERSETTINGSdict, file)
    return USERSETTINGS

def get_from_user_settings():
    '''
    Get user settings
    '''
    with open(SETTINGS_USER_PATH, 'r') as json_obj:
        try:
            USERSETTINGS = json.load(json_obj)
        except json.decoder.JSONDecodeError:
            USERSETTINGSdict = {'last_user_path': '~/Downloads'}
            with open(SETTINGS_USER_PATH, 'w') as file:
                USERSETTINGS = json.dump(USERSETTINGSdict, file)
    return USERSETTINGS

def add_to_titlovi_settings(dictionary):
    '''
    Add to Titlovi.com settings
    '''
    try:
        with open(SETTINGS_TITLOVI_PATH, 'r') as json_obj:
            USERSETTINGS = json.load(json_obj)
    except json.decoder.JSONDecodeError:
        USERSETTINGS = {'username': '', 'password': ''}
    USERSETTINGS.update(dictionary)
    with open(SETTINGS_TITLOVI_PATH, 'w') as file:
        json.dump(USERSETTINGS ,file)

def add_to_user_settings(dictionary):
    '''
    Add to user settings
    '''
    try:
        with open(SETTINGS_USER_PATH, 'r') as json_obj:
            USERSETTINGS = json.load(json_obj)
    except json.decoder.JSONDecodeError:
        USERSETTINGS = {'last_user_path': '~/Downloads'}
    USERSETTINGS.update(dictionary)
    with open(SETTINGS_USER_PATH, 'w') as file:
        json.dump(USERSETTINGS ,file)

def loadTitloviUserSettings(titlovi_object, json_settings):
    try:
        titlovi_object.user_token = json_settings['UserToken']
        titlovi_object.token_expiry_date = json_settings['ExpiryDate']
        titlovi_object.user_id = json_settings['UserID']
    except TypeError:
        titlovi_object.user_token = None
        titlovi_object.token_expiry_date = None
        titlovi_object.user_id = None

'''
This is main function that controls and links all sub-functions
Start infinite loop for your GUI windows and reading from them
'''
def run():
    #openSubtitlesAPI.set_API_key('CIVqd03XEgIT4ERQX0AGlUjcaFCfRdyI')
    log.info('Starting RUN function')
    # Set window flags as False
    SINGLE_FILE_MODE = False
    MULTI_FILE_MODE = False
    WINDOWSUBS = False
    MULTYFILEWINDOW = False
    OPENSUBSWINDOW = False
    TITLOVIWINDOW = False
    ABOUTWINDOW = False
    language_selected = []

    # Define main window
    window = sg.Window(title='Subbydoo', layout=main_layout, element_justification='center', icon=icon, finalize=True)
    gui_control.StatusBarUpdate(window, 'STATUSBAR4', value='v.0.0.3-alpha')

    # Start infinite loop
    while True:
        log.info('Checking for user tokens...')
        # Check for tokens from engines and display log in status on statusbar
        try:
            if openSubtitlesAPI.user_token != None:
                gui_control.StatusBarUpdate(window, 'STATUSBAR2', text_color='green')
            else:
                gui_control.StatusBarUpdate(window, 'STATUSBAR2', text_color='red')
            if titloviAPI.user_token != None:
                gui_control.StatusBarUpdate(window, 'STATUSBAR3', text_color='green')
                window['USETITLOVI'].update(disabled=False)
            else:
                gui_control.StatusBarUpdate(window, 'STATUSBAR3', text_color='red')
        except:
            pass

        log.info('Started GUI event loop')
        event, values = window.read() # Read main window
        #TITLOVI_SETTINGS = get_from_titlovi_settings()
        
        # If window is closed break the loop
        if event == sg.WIN_CLOSED:
            log.warning('Main window is closing')
            break
        
        # Get language selected
        language_selected = gui_control.language_selector(values)
        lang = ','.join(language_selected)
        log.info(f'Language set as - {lang}')

        # If user clicks on save, make changes (only for keep_on_top option)
        if event == 'Save':
            if values['KeepOnTop'] == False:
                window.keep_on_top_clear()
                log.info('Keep on top off')
            else:
                log.info('Keep on top on')
                window.keep_on_top_set()
                
        # If user wants to set up his own API key (needs work - not finished)
        if event == 'Set API key':
            pass
        
        if event == 'MultyFileWindow':
            MULTYFILEWINDOW = True
            multyFile_layout = gui_windows.multyfileSelectWindow()
            multyFile_window = sg.Window(title='Multiple file search - manual mode', layout=multyFile_layout, element_justification='center', finalize=True)

        if MULTYFILEWINDOW:
            multyWindow_event, multyWindow_values = multyFile_window.read()

        # If user selects OpenSubtitles define a window
        if event == 'OpenSubtitles':
            log.info('OpenSubtitles login window opened')
            OPENSUBSWINDOW = True
            openSubtitles_layout = gui_windows.openSubtitlesWindow()
            openSubtitles_window = sg.Window(title='OpenSubtitles.org', layout=openSubtitles_layout, element_justification='center', finalize=True)
        
        # If OpenSubtitles window is defined and True, display window
        if OPENSUBSWINDOW:
            log.info('Reading user token ...')
            try:
                if openSubtitlesAPI.user_token != None:
                    log.info('User token found')
                    openSubtitles_window['LOGINUSER'].update(visible=False)
                    openSubtitles_window['OpenSubtitlesUserID'].update(value=openSubtitlesAPI.user_id)
                    openSubtitles_window['OpenSubtitlesUserLevel'].update(value=openSubtitlesAPI.user_level)
                    openSubtitles_window['OpenSubtitlesUserAllDownloads'].update(value=openSubtitlesAPI.user_allowed_downloads)
                    openSubtitles_window['OpenSubtitlesUserVIP'].update(value=openSubtitlesAPI.user_vip)
                    openSubtitles_window['USERLOGGEDIN'].update(visible=True)
            except AttributeError:
                log.info('User token not found')
                pass

            log.info('Reading OpenSubtitles login window')
            openSubtitles_event, openSubtitles_values = openSubtitles_window.read()

            # If window is closed, break loop
            if openSubtitles_event == sg.WIN_CLOSED:
                log.warning('OpenSubtitles window closing')
                OPENSUBSWINDOW = False
                openSubtitles_window.close()
                continue
            
            # If user submits username and password, log in user and save data
            if openSubtitles_event == 'OpenSubtitlesSUBMIT':
                log.info('Submiting fo login proccess')
                # Update button state
                openSubtitles_window['OpenSubtitlesSUBMIT'].update(text='Logging in', button_color=('black', 'yellow'))
                window.refresh()
                # Get username and password from GUI
                userName = openSubtitles_values['OpenSubtitlesUSERNAME']
                passWord = openSubtitles_values['OpenSubtitlesPASSWORD']

                # Check if remember me is checked, if yes, save settings to JSON
                if openSubtitles_values['RememberMe']:
                    log.info('Saving credentials to JSON')
                    settingsManager.save_userdata('OpenSubtitles', username=userName, password=passWord)

                # Log user in
                log.info('Logging user in')
                openSubtitlesAPI.set_user(userName, passWord)
                login = openSubtitlesAPI.login_user()
                openSubtitlesAPI.proccess_login_response(login)
                openSubtitles_window['OpenSubtitlesSUBMIT'].update(text='Logged in', button_color=('green', 'white'))
                gui_control.StatusBarUpdate(window, 'STATUSBAR2', text_color='green')
                window.refresh()

            # If user selects logout, log the user out
            if openSubtitles_event == 'OpenSubtitlesLOGOUT':
                log.info('Logging user out')
                openSubtitlesAPI.logout_user()

        # If user selects Titlovi.com define a window
        if event == 'Titlovi.com':
            log.info('Titlovi login window opened')
            TITLOVIWINDOW = True
            titloviLogin_layout = gui_windows.TitloviLoginWindow()
            titloviLogin_window = sg.Window(title='Titlovi.com', layout=titloviLogin_layout, element_justification='center', finalize=True)
        
        # If Titlovi.com window is defined and True, display window
        if TITLOVIWINDOW:
            log.info('Checking for user token')
            if titloviAPI.user_token != None:
                log.info('User token found')
                titloviLogin_window['USERLOGGEDIN'].update(visible=True)
                titloviLogin_window['TitloviUSERID'].update(value=titloviAPI.user_id)
                titloviLogin_window['TitloviTOKEN'].update(value=titloviAPI.user_token)
                titloviLogin_window['LOGINUSER'].update(visible=False)
                window['USETITLOVI'].update(disabled=False)
                titloviLogin_window.refresh()

            # Read Titlovi login window (no timeout)
            log.info('Reading Titlovi login window')
            titloviLogin_event, titloviLogin_values = titloviLogin_window.read(timeout=300)

            # If window is closed, break the loop
            if titloviLogin_event == sg.WIN_CLOSED:
                log.warning('Closing window')
                TITLOVIWINDOW = False
                titloviLogin_window.close()
                continue
            print(titloviLogin_event)
            
            # If user selects submit, collect data and log user in
            if titloviLogin_event == 'LOGIN':
                log.info('Submitting credentials for log in')
                userName = titloviLogin_values['TitloviUSERNAME']
                passWord = titloviLogin_values['TitloviPASSWORD']
                # Collect data from GUI and set as atributes of instance titlovi
                titloviAPI.set_user(userName, passWord)
                # Log user in
                log.info('Logging user in')
                user = titloviAPI.login_user()
                titloviAPI.proccess_login_response(user)
                login = titloviAPI.handle_login()
                # Check if remember me is checked, if yes, save settings to JSON
                if titloviLogin_values['RememberMe']:
                    log.info('Writing credentials to JSON')
                    settingsManager.save_userdata('Titlovi', username=userName, password=passWord)
                TITLOVIWINDOW = False
                titloviLogin_window.close()
                window['USETITLOVI'].update(disabled=False)
                sg.popup_quick_message('Log in success!', font='Any 20', text_color='white')
                continue
        
        # If user selects About define a window
        if event == 'About':
            log.info('About window created')
            about_layout = gui_windows.AboutWindow()
            about_window = sg.Window(title='About', layout=about_layout, element_justification='center')
            ABOUTWINDOW = True
        
        # If About window defined and True, display window
        if ABOUTWINDOW:
            about_event, about_values = about_window.read()

            # If window closed, break the loop
            if about_event == sg.WIN_CLOSED:
                log.warning('Closing window')
                ABOUTWINDOW = False
                about_window.close()
                continue
        
        # If user selects Browse
        if event == 'BROWSE':
            log.info('User browsing for a video')
            # Check if remember last folder is checked, if yes, load path settings to JSON
            if values['RememberLastFolder']:
                USER_SETTINGS = get_from_user_settings()
                initial_f = USER_SETTINGS['last_user_path']
            # If not, set default path
            else:
                initial_f = '~/Downloads'

            # Get file path(s) (Popup window)
            file_paths = sg.popup_get_file('Please select a file or files', 
                                            title='Browse', 
                                            multiple_files=True, 
                                            history=True,
                                            default_extension='.mkv',
                                            no_window=False,
                                            initial_folder=initial_f,
                                            file_types=(('Video files', '.avi'),('Video files', '.mkv'),),
                                            background_color='#7E8D85',
                                            text_color='black',
                                            keep_on_top=True)
            # If file paths not selected, do not execute further
            if file_paths == None:
                log.warning('File paths do not exist')
                continue

            # Split file path(s)
            file_path = file_paths.split(';')

            # Check if Remember Last Folder is checked, if yes, save settings to JSON
            if values['RememberLastFolder']:
                file_directory = os.path.dirname(file_path[0])
                last_folder_set = {'last_user_path': file_directory}
                add_to_user_settings(last_folder_set)
            # Check to see if there is one or more paths selected and set mode acording to check
            if len(file_path) > 1:
                log.info('MODE - Multiple files')
                SINGLE_FILE_MODE = False
                MULTI_FILE_MODE = True
            else:
                log.info('MODE - Single file')
                SINGLE_FILE_MODE = True
                MULTI_FILE_MODE = False
                path = file_path[0]
                log.info('Getting file hash')
                file_hash = GetFileHash(path)
                file_size = GetFileSize(path)
                log.info('Defining Movie object')
                movie = Movie(file_size, file_hash, path, ntpath.basename(path))
                log.info('Setting Movie details from filename')
                movie.set_from_filename()
        
        # If user selects search for subtitles and is single file and quickmode is off
        if event == 'SEARCHFORSUBS' and SINGLE_FILE_MODE and values['QuickMode'] == False:
            log.info('START CONDITIONS: SINGLE FILE MODE - QUICKMODE OFF')
            # Check for engines selected
            engines = []
            open_subs = []
            titlovi_subs = []
            engines = gui_control.select_engine(values)
            log.info(f'Set engines: {engines}')

            # Iterate thru engines and search with selected
            for engine in engines:
                # If engine is OpenSubtitles
                if engine == 'OpenSubtitles':
                    log.info('Starting OpenSubtitles search')
                    # Set instance name for OpenSubtitles
                    movie_title = movie.title # Get movie title
                    # Check for movie kind and make payload accordingly
                    response = openSubtitlesAPI.search_for_subtitle(languages=lang, moviehash=movie.file_hash, query=movie_title, year=movie.year)
                    # Search OpenSubtitles server with payload
                    openSubtitlesAPI.proccess_subtitle_search_response(response)
                    results = []
                    for sub in openSubtitlesAPI.data:
                        results.append(sub)
                    log.info(f'Found {len(results)} results on OpenSubtitles')
                    # Enumerate results and put them in list
                    log.info('Making objects from results')
                    for nmb, subtitle in enumerate(results):
                        name = nmb
                        name = ProccessOpenSubtitlesSubs()
                        name.make_objects_from_subtitles(subtitle)
                        open_subs.append(name)
                # If engine is Titlovi.com
                if engine == 'Titlovi.com':
                    log.info('Starting Titlovi search')
                    languages = titloviAPI.handle_language_conversion(lang)
                    payload = titloviAPI.prepare_payload(query=movie.title)
                    for language in languages:
                        response = titloviAPI.search_for_subtitles(payload, language)
                        titloviAPI.proccess_subtitle_search_response(response)
                        for nmb, subtitle in enumerate(titloviAPI.subtitles):
                            name = nmb
                            name = ProccessTitloviSubs()
                            name.proccess_subtitle_results(subtitle)
                            titlovi_subs.append(name)
                    log.info(f'Found {len(titlovi_subs)} subtitles - Titlovi')
            log.info('All engines run')

            # When all subs have been collected set up window to display the results
            log.info('Creating window for displaying subtitles')
            WINDOWSUBS = True
            single_sub_layout = gui_windows.subs_window()
            window_download_subs = sg.Window(title='Subbydoo - download subs', layout=single_sub_layout, element_justification='center', icon=icon, finalize=True)
            all_subtitles = open_subs + titlovi_subs
            subs_names = []
            log.info('Enumerating all titles to list ')
            for sub in all_subtitles:
                if sub.engine == 'OpenSubtitles':
                    subs_names.append(sub.release)
                if sub.engine == 'Titlovi':
                    subs_names.append(f'{sub.title} {sub.release}')

        # If window has been configured, display the window
        if WINDOWSUBS:
            while True:
                # Make changes to empty movie fields (upper part - movie information)
                window_download_subs['MOVIENAME'].update(movie.title)
                window_download_subs['MOVIEYEAR'].update(movie.year)
                window_download_subs['IMDBID'].update(movie.imdb_id)
                window_download_subs['KIND'].update(movie.kind)
                window_download_subs['VIDEOFILENAME'].update(movie.file_name)
                
                # Put list of subtitle names in table of subtitles in GUI
                window_download_subs['SUBSTABLE'].update(values=subs_names)

                window_download_subs['STATUSBAR'].update(value='Language selected: {}'.format(language_selected[0]))
                
                # Read the window with a timeout of 200ms
                log.info('Reading select subtitles window')
                event_subs, values_subs = window_download_subs.read()

                # If window closed, close the window and break
                if event_subs == sg.WIN_CLOSED:
                    log.warning('Closing window')
                    WINDOWSUBS = False
                    window_download_subs.close()
                    break

                # If user clicks on subtitle, get all of information about choice and display them
                if event_subs == 'SUBSTABLE':
                    with suppress(IndexError):
                        for sub_name in subs_names:
                            if sub_name == values_subs['SUBSTABLE'][0]:
                                for sub in all_subtitles:
                                    sub_selected_engine = sub.engine
                                    if sub.engine == 'OpenSubtitles' and sub.release == sub_name:
                                        sub_selected_filename = sub.file_name
                                        sub_selected_file_id = sub.file_id
                                        sub_selected_lang = sub.language
                                        window_download_subs['ENGINE'].update(sub.engine)
                                        window_download_subs['SUBNAME'].update(sub.title)
                                        window_download_subs['SUBUSERID'].update(sub.uploader_id)
                                        window_download_subs['SUBUSERNICK'].update(sub.uploader_name)
                                        if sub.uploader_name in starting_settings.trustet_uploaders:
                                            window_download_subs['TRUSTED'].update(visible=True)
                                        else:
                                            window_download_subs['TRUSTED'].update(visible=False)
                                        window_download_subs['SUBADDDATE'].update(sub.upload_date)
                                        window_download_subs['SUBUSERCOMMENT'].update(sub.comments)
                                        window_download_subs['SUBEXTENSION'].update(sub.type)
                                        window_download_subs['SUBLANG'].update(sub.language)
                                        window_download_subs['SUBDOWNCOUNT'].update(str(sub.download_count) + ' times')
                                    if sub.engine == 'Titlovi' and f'{sub.title} {sub.release}' == sub_name:
                                        window_download_subs['ENGINE'].update(sub.engine)
                                        window_download_subs['SUBNAME'].update(sub.title)
                                        window_download_subs['SUBADDDATE'].update(sub.date)
                                        window_download_subs['SUBLANG'].update(sub.lang)
                                        window_download_subs['SUBDOWNCOUNT'].update(str(sub.downloadCount) + ' times')
                                        window_download_subs['SUBUSERID'].update('No data from this engine')
                                        window_download_subs['SUBUSERNICK'].update('No data from this engine')
                                        window_download_subs['SUBEXTENSION'].update('No data from this engine')
                                        window_download_subs['SUBSCORE'].update('No data from this engine')
                                        sub_selected_zip_down_titlovi = sub.link
                    #window_download_subs.refresh()
                    window_download_subs['DOWNLOADSUB'].update(disabled=False)

                # If user selects download subtitle
                if event_subs == 'DOWNLOADSUB':
                    # Display popup
                    sg.popup_notify('Started download of selected subtitle', title='Downloading subtitles', display_duration_in_ms=800, fade_in_duration=100)
                    # Set start time
                    TIME_START = time.perf_counter()
                    
                    # Check for engine and run download depending on it
                    if sub_selected_engine == 'OpenSubtitles':
                        log.info('Downloading subtitle using OpenSubtitles')
                        log.info('Getting download info from API')
                        file_download = openSubtitlesAPI.prepare_download(sub_selected_file_id)
                        openSubtitlesAPI.proccess_download_response(file_download)
                        log.info('Downloading subtitle')
                        openSubtitlesAPI.download_subtitle(openSubtitlesAPI.download_link)
                        if values_subs['AppendLangCode'] == True:
                            log.debug('Appending language code to name of subtitle')
                            handle_zip.move_subtitle(mode='srt', source_path='downloaded/subtitle.srt', dst_path=file_path[0], append_lang_code=sub_selected_lang)
                        else:
                            handle_zip.move_subtitle(mode='srt', source_path='downloaded/subtitle.srt', dst_path=file_path[0])
                        
                    if sub_selected_engine == 'Titlovi':
                        log.info('Downloading subtitle zip using Titlovi')
                        log.info('Downloading subtitle')
                        titloviAPI.download_subtitle(sub_selected_zip_down_titlovi)
                        handle_zip.move_subtitle(mode='zip', source_path='downloaded/sub.zip', dst_path=file_path[0])

                    # Check end time
                    TIME_END = time.perf_counter()
                    time_took = round(TIME_END-TIME_START, 2)
                    log.info(f'Took {time_took} to download subtitles')
                    sg.popup_notify('File downloaded succesfully.\nYou can find your subtitle in movie folder', title='Subtitle downloaded', display_duration_in_ms=3000, fade_in_duration=100)
        
        '''
            If user selects search for subtitles and is single file and quickmode is on
            Do everything as in QuickMode off, but select first subtitle from list automatic.
        '''
        if event == 'SEARCHFORSUBS' and SINGLE_FILE_MODE and values['QuickMode'] == True:
            movie, all_subs = gui_control.search_by_single_file(values, lang, window, file_path[0])
            TIME_START = time.perf_counter()
            print('Searching single file with QuickMode on')
            print('Searching and downloading your subtitle')
            try:
                sub = all_subs[0]
            except:
                sg.popup_error('Cant find any subtitles for your language.\nPlease choose another.')
            else:
                zip_handler = handle_zip.OpenSubtitlesHandler(sub.SubFileName, sub.ZipDownloadLink, file_path[0])
                zipThread = threading.Thread(target=threads.ZipDownloaderThreaded, args=[zip_handler])
                zipThread.start()
                zipThread.join()
                sg.PopupQuickMessage('Subtitle downloaded', font='Any 18', background_color='white', text_color='black')
            TIME_END = time.perf_counter()
            time_took = round(TIME_END-TIME_START, 2)
            print(f'\n***Download took {time_took} seconds ***\n')
        
        '''
            If user selects search for subtitles and is multy-file and quickmode is on.
            Runs thru all of files listed searching for subtitles.
            Do everything as in QuickMode off, but select first subtitle from list automatic.
        '''
        if event == 'SEARCHFORSUBS' and MULTI_FILE_MODE and values['QuickMode'] == True:
            sg.popup_quick_message('Preparing ...\nPlease wait', font='Any 14', background_color='white', text_color='black')
            TIME_START = time.perf_counter()
            print(f'*** Ready to download {len(file_path)} subtitles ***')
            window['WORKINGSTRING'].update(visible=True)
            window['PROGRESSBAR'].update(current_count=0, max=len(file_path))
            treads1 = []
            treads2 = []
            subs_list = []
            window['WORKINGSTRING'].update(value='Step 1 of 4')
            for file in range(len(file_path)):
                print(f'Threading search of subtitle {file+1} of {len(file_path)}')
                movieThread = threading.Thread(target=threads.search_by_multy_file, args=[gui_control.OpenSubtitlesSearchAlg, file_path[file], lang, file+1])
                movieThread.start()
                treads1.append(movieThread)
                window['PROGRESSBAR'].update(current_count=file+1)
            window['WORKINGSTRING'].update(value='Step 2 of 4')
            for sub in range(len(treads1)):
                subtitle = threads.subsQueve.get()
                subs_list.append(subtitle)
                window['PROGRESSBAR'].update(current_count=sub+1)
            window['WORKINGSTRING'].update(value='Step 3 of 4')
            for sub in range(len(subs_list)):
                print(f'Threading download of subtitle {sub+1} of {len(subs_list)}')
                zip_handler = handle_zip.OpenSubtitlesHandler(subs_list[sub].SubFileName, subs_list[sub].ZipDownloadLink, file_path[sub])
                zipThread = threading.Thread(target=threads.ZipDownloaderThreaded, args=[zip_handler, sub+1])
                zipThread.start()
                treads2.append(zipThread)
                window['PROGRESSBAR'].update(current_count=sub+1)
            print('\n---------- WAITING FOR FILE DOWNLOAD TO COMPLETE ----------\n')
            window['WORKINGSTRING'].update(value='Step 4 of 4')
            for number, thread in enumerate(treads1):
                thread.join()
            for number, thread in enumerate(treads2):
                thread.join()
                window['PROGRESSBAR'].update(current_count=number+1)
            zip_handler.delete_remains()
            TIME_END = time.perf_counter()
            time_took = round(TIME_END-TIME_START, 2)
            print(f'\n*** Took {time_took} to download subtitles ***\n')
            window['WORKINGSTRING'].update(visible=False)
            window['PROGRESSBAR'].update(current_count=0)
            sg.PopupQuickMessage('All subtitles downloaded', font='Any 18', background_color='white', text_color='black')

    window.close() # Closes main window
    return

