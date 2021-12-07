# Importing modules
from contextlib import suppress
import json
import os
import shutil
import threading
import PySimpleGUI as sg
from tkinter.constants import E, FALSE
from PySimpleGUI.PySimpleGUI import user_settings
from SubtitleSearcher.data.titlovi_com import TitloviCom
from SubtitleSearcher.data import opeSubtitle_new as OpenS
from SubtitleSearcher.data import handle_zip, starting_settings
from SubtitleSearcher.data import movies
from SubtitleSearcher import gui_control, gui_windows, threads
import platform
import time

# Setting default paths for setting files in JSON format
SETTINGS_OSUBTITLES_PATH = 'SubtitleSearcher/data/user_settings/OpenSubtitles_settings.json'
SETTINGS_TITLOVI_PATH = 'SubtitleSearcher/data/user_settings/Titlovi_settings.json'
SETTINGS_USER_PATH = 'SubtitleSearcher/data/user_settings/User_settings.json'

# Instantiating objects to use
openSubs = OpenS.OpenSubtitlesAPI()
titlovi = TitloviCom()

# Set starting settings
def OpenSubtitles_starting_settings():
    f = open(SETTINGS_OSUBTITLES_PATH, 'w')
    start_setting = {'username': '', 'password': ''}
    json.dump(start_setting, f)
    f.close()

def Titlovi_starting_settings():
    f = open(SETTINGS_TITLOVI_PATH, 'w')
    start_setting = {'username': '', 'password': ''}
    json.dump(start_setting, f)
    f.close()

def User_starting_settings():
    f = open(SETTINGS_USER_PATH, 'w')
    start_setting = {'last_user_path': '~/Downloads'}
    json.dump(start_setting, f)
    f.close()

# Set AutoLogin
def AutoLogin_Titlovi():
    '''
    Autologin function for Titlovi.com engine
    '''
    f = open(SETTINGS_TITLOVI_PATH, 'r')
    
    username = ''
    password = ''
    try:
        settings = json.load(f)
    except:
        print('AutoLogin - No valid settings found - Titlovi')
    else:
        print('AutoLogin - Settings found - Titlovi')
        username = settings['username']
        password = settings['password']
    finally:
        f.close()
    print('AutoLogin - logging user in - Titlovi')
    titlovi.username = username
    titlovi.password = password
    if titlovi.handle_login():
        print('AutoLogin - User logged in - Titlovi')
    else:
        print('AutoLogin - User not logged in - Titlovi')

def AutoLogin_OpenSubtitles():
    '''
    Autologin function for OpenSubtitles.com engine
    '''
    f = open(SETTINGS_OSUBTITLES_PATH, 'r')
    
    username = ''
    password = ''
    try:
        settings = json.load(f)
    except:
        print('AutoLogin - No valid settings found - OpenSubtitles')
    else:
        print('AutoLogin - Settings found - OpenSubtitles')
        username = settings['username']
        password = settings['password']
    finally:
        f.close()
    print('AutoLogin - logging user in - OpenSubtitles')
    if openSubs.user_login(username, password):
        print('AutoLogin - User logged in - OpenSubtitles')
    else:
        print('AutoLogin - User not logged in - OpenSubtitles')

# Check for folders and files at start of program
def StartUp():
    '''
    Check for folders and files needed for startup.
    If there are none, make them
    '''
    os.makedirs('SubtitleSearcher/data/user_settings', exist_ok=True)
    if not os.path.isfile(SETTINGS_OSUBTITLES_PATH):
        OpenSubtitles_starting_settings()
    if not os.path.isfile(SETTINGS_TITLOVI_PATH):
        Titlovi_starting_settings()
    if not os.path.isfile(SETTINGS_USER_PATH):
        User_starting_settings()

# Run StartUp function
StartUp()

# Thread AutoLogin scripts - as they are deamon threads there is no need to join them
AutoLoginOpenS_thread = threading.Thread(target=AutoLogin_OpenSubtitles, daemon=True)
AutoLoginOpenS_thread.start()
AutoLoginTitlovi_thread = threading.Thread(target=AutoLogin_Titlovi, daemon=True)
AutoLoginTitlovi_thread.start()

# Check for system and use appropriate image for icon
system = platform.system()
if system == 'Windows':
    icon = 'images/image.ico'
if system == 'Linux':
    icon = 'images/image.png'
main_layout = gui_windows.main_window()

# Display intro dialog
gui_control.intro_dialog()


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
    # Set window flags as False
    SINGLE_FILE_MODE = False
    MULTI_FILE_MODE = False
    WINDOWSUBS = False
    OPENSUBSWINDOW = False
    TITLOVIWINDOW = False
    ABOUTWINDOW = False
    language_selected = []

    # Define main window
    window = sg.Window(title='Subbydoo', layout=main_layout, element_justification='center', icon=icon, finalize=True)

    # Check for tokens from engines and display log in status on statusbar
    try:
        if openSubs.user_token != None:
            gui_control.StatusBarUpdate(window, 'STATUSBAR2', text_color='green')
        else:
            gui_control.StatusBarUpdate(window, 'STATUSBAR2', text_color='red')
        if titlovi.user_token != None:
            gui_control.StatusBarUpdate(window, 'STATUSBAR3', text_color='green')
            window['USETITLOVI'].update(disabled=False)
        else:
            gui_control.StatusBarUpdate(window, 'STATUSBAR3', text_color='red')
    except:
        pass
    gui_control.StatusBarUpdate(window, 'STATUSBAR4', value='v.0.0.3-alpha')

    # Start infinite loop
    while True:
        event, values = window.read(timeout=300) # Read main window (timeout is 300ms)
        TITLOVI_SETTINGS = get_from_titlovi_settings()

        # If window is closed break the loop
        if event == sg.WIN_CLOSED:
            break
        
        # Get language selected
        language_selected = gui_control.language_selector(values)
        lang = ','.join(language_selected)

        # If user clicks on save, make changes (only for keep_on_top option)
        if event == 'Save':
            if values['KeepOnTop'] == False:
                window.keep_on_top_clear()
            else:
                window.keep_on_top_set()

        # If user wants to set up his own API key (needs work - not finished)
        if event == 'Set API key':
            pass

        # If user selects OpenSubtitles define a window
        if event == 'OpenSubtitles':
            OPENSUBSWINDOW = True
            openSubtitles_layout = gui_windows.openSubtitlesWindow()
            openSubtitles_window = sg.Window(title='OpenSubtitles.org', layout=openSubtitles_layout, element_justification='center', finalize=True)
        
        # If OpenSubtitles window is defined and True, display window
        if OPENSUBSWINDOW:
            try:
                if openSubs.user_token != None:
                        openSubtitles_window['LOGINUSER'].update(visible=False)
                        openSubtitles_window['OpenSubtitlesUserID'].update(value=openSubs.user_id)
                        openSubtitles_window['OpenSubtitlesUserLevel'].update(value=openSubs.user_level)
                        openSubtitles_window['OpenSubtitlesUserAllDownloads'].update(value=openSubs.user_allowed_downloads)
                        openSubtitles_window['OpenSubtitlesUserVIP'].update(value=openSubs.user_vip)
                        openSubtitles_window['USERLOGGEDIN'].update(visible=True)
            except AttributeError:
                pass
            openSubtitles_event, openSubtitles_values = openSubtitles_window.read()

            # If window is closed, break loop
            if openSubtitles_event == sg.WIN_CLOSED:
                OPENSUBSWINDOW = False
                openSubtitles_window.close()
                continue
            
            # If user submits username and password, log in user and save data
            if openSubtitles_event == 'OpenSubtitlesSUBMIT':
                # Update button state
                openSubtitles_window['OpenSubtitlesSUBMIT'].update(text='Logging in', button_color=('black', 'yellow'))
                window.refresh()
                # Get username and password from GUI
                userName = openSubtitles_values['OpenSubtitlesUSERNAME']
                passWord = openSubtitles_values['OpenSubtitlesPASSWORD']

                # Check if remember me is checked, if yes, save settings to JSON
                if openSubtitles_values['RememberMe']:
                    new_setting = {'username': userName, 'password': passWord}
                    f = open(SETTINGS_OSUBTITLES_PATH, 'w')
                    json.dump(new_setting, f)
                    f.close()

                # Log user in
                if openSubs.user_login(userName, passWord):
                    openSubtitles_window['OpenSubtitlesSUBMIT'].update(text='Logged in', button_color=('green', 'white'))
                    gui_control.StatusBarUpdate(window, 'STATUSBAR2', text_color='green')
                    window.refresh()
                # Wrong username / password ??
                else:
                    sg.popup_quick_message('There was a problem logging you in! Please try again.', font='Any 20', text_color='white')
                    openSubtitles_window['OpenSubtitlesSUBMIT'].update(text='Log in', button_color=('white', 'red'))
                    window.refresh()

            # If user selects logout, log the user out
            if openSubtitles_event == 'OpenSubtitlesLOGOUT':
                openSubs.user_logout()

        # If user selects Titlovi.com define a window
        if event == 'Titlovi.com':
            TITLOVIWINDOW = True
            titloviLogin_layout = gui_windows.TitloviLoginWindow()
            titloviLogin_window = sg.Window(title='Titlovi.com', layout=titloviLogin_layout, element_justification='center', finalize=True)
            try:
                TokExp, DYSleft = titlovi.check_for_expiry_date()
            except TypeError:
                pass
        
        # If Titlovi.com window is defined and True, display window
        if TITLOVIWINDOW:
            if titlovi.user_token != None:
                titloviLogin_window['USERLOGGEDIN'].update(visible=True)
                titloviLogin_window['TitloviUSERID'].update(value=titlovi.user_id)
                titloviLogin_window['TitloviTOKEN'].update(value=titlovi.user_token)
                titloviLogin_window['TitloviEXPIRY'].update(value=DYSleft)
                titloviLogin_window['LOGINUSER'].update(visible=False)
                window['USETITLOVI'].update(disabled=False)
                titloviLogin_window.refresh()

            # Read Titlovi login window (no timeout)
            titloviLogin_event, titloviLogin_values = titloviLogin_window.read()

            # If window is closed, break the loop
            if titloviLogin_event == sg.WIN_CLOSED:
                TITLOVIWINDOW = False
                titloviLogin_window.close()
                continue
            
            # If user selects submit, collect data and log user in
            if titloviLogin_event == 'TitloviSUBMIT':
                userName = titloviLogin_values['TitloviUSERNAME']
                passWord = titloviLogin_values['TitloviPASSWORD']
                # Collect data from GUI and set as atributes of instance titlovi
                titlovi.username = userName
                titlovi.password = passWord
                # Log user in
                login = titlovi.handle_login()
                # Check if remember me is checked, if yes, save settings to JSON
                if titloviLogin_values['RememberMe']:
                    new_setting = {'username': userName, 'password': passWord}
                    f = open(SETTINGS_TITLOVI_PATH, 'w')
                    json.dump(new_setting, f)
                    f.close()
                
                # If login True, set data
                if login != None:
                    titlovi.set_user_login_details(login)
                    new_user = {'UserToken': titlovi.user_token,
                                'ExpiryDate': titlovi.token_expiry_date,
                                'UserID': titlovi.user_id}
                    add_to_titlovi_settings(new_user)
                    expired_token, days_left = titlovi.check_for_expiry_date()
                # Wrong username / password
                else:
                    sg.popup_ok('Invalid username / password !\nPlease check your login details.', title='Wrong username/password', font='Any 16')
                    continue
                TITLOVIWINDOW = False
                titloviLogin_window.close()
                window['USETITLOVI'].update(disabled=False)
                sg.popup_quick_message('Log in success!', font='Any 20', text_color='white')
                continue
        
        # If user selects About define a window
        if event == 'About':
            about_layout = gui_windows.AboutWindow()
            about_window = sg.Window(title='About', layout=about_layout, element_justification='center')
            ABOUTWINDOW = True
        
        # If About window defined and True, display window
        if ABOUTWINDOW:
            about_event, about_values = about_window.read()

            # If window closed, break the loop
            if about_event == sg.WIN_CLOSED:
                ABOUTWINDOW = False
                about_window.close()
                continue
        
        # If user selects Browse
        if event == 'BROWSE':
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
                                            background_color='green',
                                            text_color='black',
                                            keep_on_top=True)
            # If file paths not selected, do not execute further
            if file_paths == None:
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
                SINGLE_FILE_MODE = False
                MULTI_FILE_MODE = True
            else:
                SINGLE_FILE_MODE = True
                MULTI_FILE_MODE = False
            path = file_path[0]
            # Set movie instance from selected file
            movie = gui_control.define_movie(path)
        
        # If user selects search for subtitles and is single file and quickmode is off
        if event == 'SEARCHFORSUBS' and SINGLE_FILE_MODE and values['QuickMode'] == False:
            # Check for engines selected
            engines = []
            engines = gui_control.select_engine(values)

            # Iterate thru engines and search with selected
            for engine in engines:
                # If engine is OpenSubtitles
                if engine == 'OpenSubtitles':
                    # Set instance name for OpenSubtitles
                    open_search = OpenS.SearchForSubs()
                    movie_title = movie.title # Get movie title

                    # Check for movie kind and make payload accordingly
                    if movie.kind == 'movie':
                        payload = open_search.set_payload(imdb_id=movie.imdb_id, languages=lang, moviehash=movie.file_hash,  query=movie_title.lower(), year=movie.year)
                    elif movie.kind == 'tv series' or movie.kind == 'season':
                        payload = open_search.set_payload(moviehash=movie.file_hash, query=movie.title, imdb_id=movie.imdb_id, languages=lang, episode_number=movie.episode, season_number=movie.season)
                    # Search OpenSubtitles server with payload
                    open_search.search_subtitles(payload)
                    # Get results
                    results = open_search.data
                    open_subs = []
                    # Enumerate results and put them in list
                    for nmb, result in enumerate(results):
                        nmb = OpenS.OpenSubtitlesSubtitleResults(result)
                        open_subs.append(nmb)
                # If engine is Titlovi.com
                if engine == 'Titlovi.com':
                    try:
                        titlovi_subs = gui_control.search_titlovi(lang, movie, titlovi)
                    except UnboundLocalError:
                        sg.popup_error('User is not validated.\nPlease validate your account to use Titlovi.com')
            print('Searching single file with QuickMode off')

            # When all subs have been collected set up window to display the results
            WINDOWSUBS = True
            single_sub_layout = gui_windows.subs_window()
            window_download_subs = sg.Window(title='Subbydoo - download subs', layout=single_sub_layout, element_justification='center', icon=icon, finalize=True)
            
        # If window has been configured, display the window
        if WINDOWSUBS:
            # Make changes to empty movie fields (upper part - movie information)
            window_download_subs['MOVIENAME'].update(movie.title)
            window_download_subs['MOVIEYEAR'].update(movie.year)
            window_download_subs['IMDBID'].update(movie.imdb_id)
            window_download_subs['KIND'].update(movie.kind)
            window_download_subs['VIDEOFILENAME'].update(movie.file_name)

            # Make list of all subtitles objects from engines
            subs_list = []
            for engine in engines:
                if engine == 'OpenSubtitles':
                    for q in range(len(open_subs)):
                        with suppress(AttributeError): subs_list.append(open_subs[q])
                if engine == 'Titlovi.com':
                    for w in range(len(titlovi_subs)):
                        with suppress(AttributeError): subs_list.append(titlovi_subs[w])
            # Make a list of all subtitles names to display in list
            subs_names = []
            for sub in subs_list:
                if sub.engine == 'OpenSubtitles':
                    subs_names.append(sub.release)
                if sub.engine == 'Titlovi':
                    if sub.season >= 0 or sub.episode >= 0:
                        subs_names.append(f'{sub.title} S{str(sub.season)}E{str(sub.episode)}')
                    else:
                        subs_names.append(f'{sub.title} {sub.release}')
            
            # Put list of subtitle names in table of subtitles in GUI
            window_download_subs['SUBSTABLE'].update(values=subs_names)

            # Read the window with a timeout of 200ms
            event_subs, values_subs = window_download_subs.read()
            window_download_subs['STATUSBAR'].update(value='Language selected: {}'.format(language_selected[0]))
            
            # If window closed, close the window and break
            if event_subs == sg.WIN_CLOSED:
                WINDOWSUBS = False
                window_download_subs.close()
                continue

            # If user clicks on subtitle, get all of information about choice and display them
            if event_subs == 'SUBSTABLE':
                with suppress(IndexError):
                    for sub_name in subs_names:
                        if sub_name == values_subs['SUBSTABLE'][0]:
                            for sub in subs_list:
                                sub_selected_engine = sub.engine
                                if sub.engine == 'OpenSubtitles' and sub.release == sub_name:
                                    sub_selected_filename = sub.file_name
                                    sub_selected_file_id = sub.file_id
                                    sub_selected_lang = sub.language
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
                                    window_download_subs['SUBNAME'].update(sub.title)
                                    window_download_subs['SUBADDDATE'].update(sub.date)
                                    window_download_subs['SUBLANG'].update(sub.lang)
                                    window_download_subs['SUBDOWNCOUNT'].update(str(sub.downloadCount) + ' times')
                                    window_download_subs['SUBUSERID'].update('')
                                    window_download_subs['SUBUSERNICK'].update('')
                                    window_download_subs['SUBUSERCOMMENT'].update('')
                                    window_download_subs['SUBEXTENSION'].update('')
                                    window_download_subs['SUBSCORE'].update('')
                                    sub_selected_zip_down_titlovi = sub.link
                window_download_subs['DOWNLOADSUB'].update(disabled=False)
                window_download_subs.refresh()

            # If user selects download subtitle
            if event_subs == 'DOWNLOADSUB':
                # Display popup
                sg.popup_notify('Started download of selected subtitle', title='Downloading subtitles', display_duration_in_ms=800, fade_in_duration=100)
                # Set start time
                TIME_START = time.perf_counter()
                
                # Check for engine and run download depending on it
                if sub_selected_engine == 'OpenSubtitles':
                    download = OpenS.DownloadSubtitle()
                    download.get_info(sub_selected_file_id, user_token=openSubs.user_token)
                    download.download_subtitle()
                    if values_subs['AppendLangCode'] == True:
                        handle_zip.move_subtitle('downloaded/subtitle.srt', file_path[0], append_lang_code=sub_selected_lang)
                    else:
                        handle_zip.move_subtitle('downloaded/subtitle.srt', file_path[0])
                    
                elif sub_selected_engine == 'Titlovi':
                    file_handler = handle_zip.TitloviFileHandler()
                    file_handler.download(sub_selected_zip_down_titlovi)
                    if values_subs['AppendLangCode'] == True:
                        file_handler.move_file(file_path[0], append_lang_code=lang)
                    else:
                        file_handler.move_file(file_path[0])

                # Check end time
                TIME_END = time.perf_counter()
                time_took = round(TIME_END-TIME_START, 2)
                print(f'\n*** Took {time_took} to download subtitles ***\n')
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