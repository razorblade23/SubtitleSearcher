# Importing modules
from contextlib import suppress
import json
from logging import disable
import os
import threading
import PySimpleGUI as sg
from tkinter.constants import E, FALSE

from PySimpleGUI.PySimpleGUI import user_settings
from SubtitleSearcher.data.titlovi_com import TitloviCom
from SubtitleSearcher.data import handle_zip, starting_settings
from SubtitleSearcher import gui_control, gui_windows, threads
import platform
import time

if not os.path.isdir('SubtitleSearcher/data/user_settings'):
    os.makedirs('SubtitleSearcher/data/user_settings')

if not os.path.isfile('SubtitleSearcher/data/user_settings/user_settings.json'):
    settings_path = 'SubtitleSearcher/data/user_settings/user_settings.json'
    with open(settings_path, 'w') as file:
        last_folder_set = {'last_user_path': '~/Downloads'}
        user_set = json.dump(last_folder_set, file)

system = platform.system()
if system == 'Windows':
    icon = 'SubtitleSearcher/static/images/image.ico'
if system == 'Linux':
    icon = 'SubtitleSearcher/static/images/image.png'

JSON_USER_SETTINGS_PATH = 'SubtitleSearcher/data/user_settings/user_settings.json'

SINGLE_FILE_MODE = False
MULTI_FILE_MODE = False
WINDOWSUBS = False
language_selected = []

main_layout = gui_windows.main_window()

gui_control.intro_dialog()

def getUserSettings():
    with open(JSON_USER_SETTINGS_PATH, 'r') as json_obj:
        try:
            USERSETTINGS = json.load(json_obj)
        except json.decoder.JSONDecodeError:
            USERSETTINGSdict = {'last_user_path': '~/Downloads'}
            with open(JSON_USER_SETTINGS_PATH, 'w') as file:
                USERSETTINGS = json.dump(USERSETTINGSdict, file)
    return USERSETTINGS

def add_to_user_settings(dictionary):
    try:
        with open(JSON_USER_SETTINGS_PATH, 'r') as json_obj:
            USERSETTINGS = json.load(json_obj)
    except json.decoder.JSONDecodeError:
        USERSETTINGS = {'last_user_path': '~/Downloads'}
    USERSETTINGS.update(dictionary)
    with open(JSON_USER_SETTINGS_PATH, 'w') as file:
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


# Start infinite loop for your GUI windows and reading from them
def run():
    global WINDOWSUBS, language_selected, SINGLE_FILE_MODE, MULTI_FILE_MODE
    window = sg.Window(title='Subbydoo', layout=main_layout, element_justification='center', icon=icon, finalize=True)

    titlovi = TitloviCom()
    USER_SETTINGS = getUserSettings()
    try:
        loadTitloviUserSettings(titlovi, USER_SETTINGS)
    except KeyError:
        token = None
    else:
        token = titlovi.user_token

    if token != None:
        expired_token, days_left = titlovi.check_for_expiry_date()
        UserGuiRegistered(window, titlovi, days_left)
    else:
        print('No token detected')

    while True:
        event, values = window.read(timeout=300)
        #print(f'Currently active threads: {threading.active_count()}\n')
        if event == sg.WIN_CLOSED:
            break
        if token != None:
            expired_token, days_left = titlovi.check_for_expiry_date()
            gui_control.StatusBarMainUpdate(window, f'SubbyDoo is ready.\nTitlovi.com logged in -->User ID: {titlovi.user_id} -->Token expired: {expired_token}, days left: {days_left}')
        else:
            gui_control.StatusBarMainUpdate(window, f'SubbyDoo is ready\nUser is not logged in')
        language_selected = gui_control.language_selector(values)
        lang = language_selected[0]
        gui_control.StatusBarVersionUpdate(window, 'v.0.0.3-alpha')
        if event == 'Save':
            if values['KeepOnTop'] == False:
                window.keep_on_top_clear()
            else:
                window.keep_on_top_set()

        if event == 'OpenSubtitles':
            openSubtitles_layout = gui_windows.openSubtitlesWindow()
            openSubtitles_window = sg.Window(title='OpenSubtitles.org', layout=openSubtitles_layout)
            openSubtitles_event, openSubtitles_values = openSubtitles_window.read()

        if event == 'LoginUserTitlovi':
            user_name = values['titloviUSERNAME']
            password = values['titloviPASS']
            if token == None:
                titlovi.username = user_name
                titlovi.password = password
                login = titlovi.handle_login()
                if login != None:
                    titlovi.set_user_login_details(login)
                    new_user = {'UserToken': titlovi.user_token,
                                'ExpiryDate': titlovi.token_expiry_date,
                                'UserID': titlovi.user_id}
                    add_to_user_settings(new_user)
                    expired_token, days_left = titlovi.check_for_expiry_date()
                else:
                    sg.popup_ok('Invalid username / password !\nPlease check your login details.', title='Wrong username/password', font='Any 16')
                    continue
                window['LoginUserTitlovi'].update(text='USER VALIDATED', button_color=('white', 'green'))
                UserGuiRegistered(window, titlovi, days_left)
            else:
                window['USETITLOVI'].update(disabled=False)
            window.refresh()

        if event == 'BROWSE':
            if values['RememberLastFolder']:
                USER_SETTINGS = getUserSettings()
                initial_f = USER_SETTINGS['last_user_path']
            else:
                initial_f = '~/Downloads'

            file_paths = sg.popup_get_file('Please select a file or files', 
                                            title='Browse', 
                                            multiple_files=True, 
                                            history=True,
                                            default_extension='.mkv',
                                            no_window=False,
                                            initial_folder=initial_f,
                                            file_types=(('Video files', '.avi'),('Video files', '.mkv'),))
            if file_paths == None:
                continue
            file_path = file_paths.split(';')
            if values['RememberLastFolder']:
                file_directory = os.path.dirname(file_path[0])
                last_folder_set = {'last_user_path': file_directory}
                add_to_user_settings(last_folder_set)
            if len(file_path) > 1:
                SINGLE_FILE_MODE = False
                MULTI_FILE_MODE = True
            else:
                SINGLE_FILE_MODE = True
                MULTI_FILE_MODE = False
        
        if event == 'SEARCHFORSUBS' and SINGLE_FILE_MODE and values['QuickMode'] == False:
            engines = []
            engines = gui_control.select_engine(values)
            path = file_path[0]
            movie = gui_control.define_movie(path)
            window['STATUSBAR'].update(f'Movie name: {movie.title} - IMDB ID: {movie.imdb_id}')
            for engine in engines:
                if engine == 'OpenSubtitles':
                    open_subs = gui_control.search_opensubs(lang, movie)
                if engine == 'Titlovi.com':
                    try:
                        titlovi_subs = gui_control.search_titlovi(lang, movie, titlovi)
                    except UnboundLocalError:
                        sg.popup_error('User is not validated.\nPlease validate your account to use Titlovi.com')
            print('Searching single file with QuickMode off')
            WINDOWSUBS = True
            single_sub_layout = gui_windows.subs_window()
            window_download_subs = sg.Window(title='Subbydoo - download subs', layout=single_sub_layout, element_justification='center', icon=icon, finalize=True)
            

        if WINDOWSUBS:
            window_download_subs['MOVIENAME'].update(movie.title)
            window_download_subs['MOVIEYEAR'].update(movie.year)
            window_download_subs['IMDBID'].update(movie.imdb_id)
            window_download_subs['KIND'].update(movie.kind)
            window_download_subs['VIDEOFILENAME'].update(movie.file_name)
            subs_list = []
            for engine in engines:
                if engine == 'OpenSubtitles':
                    for q in range(len(open_subs)):
                        with suppress(AttributeError): subs_list.append(open_subs[q])
                if engine == 'Titlovi.com':
                    for w in range(len(titlovi_subs)):
                        with suppress(AttributeError): subs_list.append(titlovi_subs[w])
            subs_names = []
            for sub in subs_list:
                if sub.engine == 'OpenSubtitles':
                    subs_names.append(sub.MovieReleaseName)
                if sub.engine == 'Titlovi':
                    if sub.season >= 0 or sub.episode >= 0:
                        subs_names.append(f'{sub.title} S{str(sub.season)}E{str(sub.episode)}')
                    else:
                        subs_names.append(f'{sub.title} {sub.release}')
            window_download_subs['SUBSTABLE'].update(values=subs_names)

            if movie.kind == 'tv series' or movie.kind == 'episode':
                window_download_subs['TVSERIESINFO'].update(visible=False)
                window_download_subs['SEASON'].update(value=movie.season)
                window_download_subs['EPISODE'].update(value=movie.episode)

            event_subs, values_subs = window_download_subs.read()
            window_download_subs['STATUSBAR'].update(value='Language selected: {}'.format(language_selected[0]))
            
            if event_subs == sg.WIN_CLOSED:
                WINDOWSUBS = False
                window_download_subs.close()
                continue

            if event_subs == 'SUBSTABLE':
                with suppress(IndexError):
                    for sub_name in subs_names:
                        if sub_name == values_subs['SUBSTABLE'][0]:
                            for sub in subs_list:
                                sub_selected_engine = sub.engine
                                if sub.engine == 'OpenSubtitles' and sub.MovieReleaseName == sub_name:
                                    sub_selected_filename = sub.SubFileName
                                    sub_selected_zip_down_open = sub.ZipDownloadLink
                                    window_download_subs['SUBNAME'].update(sub.SubFileName)
                                    window_download_subs['SUBUSERID'].update(sub.UserID)
                                    window_download_subs['SUBUSERNICK'].update(sub.UserNickName)
                                    if sub.UserNickName in starting_settings.trustet_uploaders:
                                        window_download_subs['TRUSTED'].update(visible=True)
                                    else:
                                        window_download_subs['TRUSTED'].update(visible=False)
                                    window_download_subs['SUBADDDATE'].update(sub.SubAddDate)
                                    window_download_subs['SUBUSERCOMMENT'].update(sub.SubAuthorComment)
                                    window_download_subs['SUBEXTENSION'].update(sub.SubFormat)
                                    window_download_subs['SUBLANG'].update(sub.LanguageName)
                                    window_download_subs['SUBDOWNCOUNT'].update(str(sub.SubDownloadsCnt) + ' times')
                                    window_download_subs['SUBSCORE'].update(str(sub.Score) + ' %')
                                    if sub.Score > 0 and sub.Score < 10:
                                        window_download_subs['SUBSCORE'].update(text_color='black')
                                    elif sub.Score > 10 and sub.Score < 30:
                                        window_download_subs['SUBSCORE'].update(text_color='red')
                                    elif sub.Score > 30 and sub.Score < 60:
                                        window_download_subs['SUBSCORE'].update(text_color='orange')
                                    elif sub.Score > 60 and sub.Score < 100:
                                        window_download_subs['SUBSCORE'].update(text_color='green')
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

            if event_subs == 'DOWNLOADSUB':
                sg.popup_notify('Started download of selected subtitle', title='Downloading subtitles', display_duration_in_ms=800, fade_in_duration=100)
                TIME_START = time.perf_counter()
                if sub_selected_engine == 'OpenSubtitles':
                    file_handler = handle_zip.OpenSubtitlesHandler()
                    file_handler.download_zip(sub_selected_zip_down_open)
                    file_handler.extract_zip()
                    file_handler.move_files(file_path[0], sub_selected_filename)
                    #zip_handler = handle_zip.OpenSubtitlesHandler(sub_selected_zip_down_open)
                    #zipThread = threading.Thread(target=threads.ZipDownloaderThreaded, args=[zip_handler])
                    #zipThread.start()
                    #zipThread.join()
                elif sub_selected_engine == 'Titlovi':
                    file_handler = handle_zip.TitloviFileHandler()
                    file_handler.download(sub_selected_zip_down_titlovi)
                    file_handler.move_file(file_path[0])
                TIME_END = time.perf_counter()
                time_took = round(TIME_END-TIME_START, 2)
                print(f'\n*** Took {time_took} to download subtitles ***\n')
                sg.popup_notify('File downloaded succesfully.\nYou can find your subtitle in movie folder', title='Subtitle downloaded', display_duration_in_ms=3000, fade_in_duration=100)

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


        #if values['SINGLEFILE'] != 'Browse this to select a single file !':
        #    window['SEARCHBYSINGLEFILE'].update(disabled=False)
        #
        #if values['MULTIPLEFILES'] != 'Browse this to select multiple files !':
        #    window['SEARCHBYMULTIFILE'].update(disabled=False)
            
    window.close() # Closes main window
    return

def UserGuiRegistered(window, titlovi, days_left):
    window['USETITLOVI'].update(disabled=False)
    window['ROW1'].update(value=f'User ID: {titlovi.user_id}', text_color='green')
    window['ROW2'].update(value=f'Token: {titlovi.user_token}', text_color='green')
    window['ROW3'].update(value=f'Token need refresh in {days_left} days', text_color='green')
    window['ROW4'].update(value='')