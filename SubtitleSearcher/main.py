# Importing modules
import os
import threading
import PySimpleGUI as sg
from tkinter.constants import FALSE
from SubtitleSearcher.data import handle_zip
from SubtitleSearcher import gui_control, gui_windows, threads
from contextlib import suppress
import platform

system = platform.system()
if system == 'Windows':
    icon = 'SubtitleSearcher/static/images/image.ico'
if system == 'Linux':
    icon = 'SubtitleSearcher/static/images/image.png'

WINDOWSUBS = False
language_selected = []

main_layout = gui_windows.main_window()

gui_control.intro_dialog()

# Start infinite loop for your GUI windows and reading from them
def run():
    global WINDOWSUBS, language_selected
    window = sg.Window(title='Subbydoo', layout=main_layout, element_justification='center', icon=icon, finalize=True)
    while True:
        event, values = window.read(timeout=300)
        if event == sg.WIN_CLOSED:
            break
        
        language_selected = gui_control.language_selector(values)
        lang = language_selected[0]
        gui_control.StatusBarMainUpdate(window, f'SubbyDoo is ready. | Language selected: {lang}')
        gui_control.StatusBarVersionUpdate(window, 'v.0.0.2-alpha')

        if event == 'Save':
            if values['KeepOnTop'] == False:
                window.keep_on_top_clear()
            else:
                window.keep_on_top_set()

        if values['SINGLEFILE'] != 'Browse this to select a single file !':
            window['SEARCHBYSINGLEFILE'].update(disabled=False)
        
        if values['MULTIPLEFILES'] != 'Browse this to select multiple files !':
            window['SEARCHBYMULTIFILE'].update(disabled=False)

        if event == 'SEARCHBYSINGLEFILE':
            movie, all_subs = gui_control.search_by_single_file(values, lang, window)


        ####### SINGLE FILE & QUICKMODE OFF #########
        if not WINDOWSUBS and event == 'SEARCHBYSINGLEFILE' and values['QuickMode'] == False:
            print('Searching single file with QuickMode off')
            WINDOWSUBS = True
            single_sub_layout = gui_windows.subs_window()
            window_download_subs = sg.Window(title='Subbydoo - download subs', layout=single_sub_layout, element_justification='center', icon=icon, finalize=True)
            

        ####### SINGLE FILE & QUICKMODE ON #########
        if not WINDOWSUBS and event == 'SEARCHBYSINGLEFILE' and values['QuickMode'] == True:
            print('Searching single file with QuickMode on')
            print('Searching and downloading your subtitle')
            window.refresh()
            try:
                sub = all_subs[0]
            except:
                sg.popup_error('Cant find any subtitles for your language.\nPlease choose another.')
            else:
                zip_handler = handle_zip.ZipHandler(sub.SubFileName, sub.ZipDownloadLink, values['SINGLEFILE'])
                file_download = zip_handler.download_zip()
                if file_download:
                    zip_handler.extract_zip()
                    zip_handler.move_files()
                    zip_handler.delete_remains()
                    print('Subtitle downloaded\n')
                    sg.PopupQuickMessage('Subtitle downloaded', font='Any 18', background_color='white', text_color='black')
        

        ####### MULTIPLE FILES & QUICKMODE ON #########
        if not WINDOWSUBS and event == 'SEARCHBYMULTIFILE' and values['QuickMode'] == True:
            files = values['MULTIPLEFILES']
            files_lst = files.split(';')
            print(f'*** Ready to download {len(files_lst)} subtitles ***')
            movies_list = []
            subs_list = []
            for file in range(len(files_lst)):
                movie, all_subs = gui_control.search_by_multy_file(values, files_lst[file], lang, window)
                subs_list.append(all_subs[0])
            for sub in range(len(subs_list)):
                print(f'\nDownloading subtitle {sub+1} of {len(subs_list)}')
                zip_handler = handle_zip.ZipHandler(subs_list[sub].SubFileName, subs_list[sub].ZipDownloadLink, files_lst[sub])
                file_download = zip_handler.download_zip()
                if file_download:
                    zip_handler.extract_zip()
                    zip_handler.move_files()
                    zip_handler.delete_remains()
                print(f'Subtitle downloaded')
            sg.PopupQuickMessage('All subtitles downloaded', font='Any 18', background_color='white', text_color='black')

        if WINDOWSUBS:
            event_subs, values_subs = window_download_subs.read(timeout=600)
            window_download_subs['STATUSBAR'].update(value='Subtitles found: {} | Language selected: {}'.format(len(all_subs), language_selected[0]))
            
            if event_subs == sg.WIN_CLOSED:
                WINDOWSUBS = False
                window_download_subs.close()
                continue

            if event_subs == 'SUBSTABLE':
                for sub in all_subs:
                    if sub.MovieReleaseName == values_subs['SUBSTABLE'][0]:
                        sub_selected_filename = sub.SubFileName
                        sub_selected_zip_down = sub.ZipDownloadLink
                        window_download_subs['SUBNAME'].update(sub.SubFileName)
                        window_download_subs['SUBUSERID'].update(sub.UserID)
                        window_download_subs['SUBUSERNICK'].update(sub.UserNickName)
                        window_download_subs['SUBADDDATE'].update(sub.SubAddDate)
                        window_download_subs['SUBUSERCOMMENT'].update(sub.SubAuthorComment)
                        window_download_subs['SUBEXTENSION'].update(sub.SubFormat)
                        window_download_subs['SUBLANG'].update(sub.LanguageName)
                        window_download_subs['SUBDOWNCOUNT'].update(str(sub.SubDownloadsCnt) + ' times')
                        window_download_subs['SUBSCORE'].update(str(sub.Score) + ' %')
                        #print(sub.SubFileName) # ovdje mjenjaj sto ti ispisuje
                window_download_subs['DOWNLOADSUB'].update(disabled=False)

            if event_subs == 'DOWNLOADSUB':
                sg.popup_notify('Started download of selected subtitle', title='Downloading subtitles', display_duration_in_ms=800, fade_in_duration=100)
                selected_sub = handle_zip.ZipHandler(sub_selected_filename, sub_selected_zip_down, values['SINGLEFILE'])
                downloadIt = selected_sub.download_zip()
                if downloadIt:
                    selected_sub.extract_zip()
                    selected_sub.move_files()
                    selected_sub.delete_remains()
                    sg.popup_notify('File downloaded succesfully.\nYou can find your subtitle in movie folder', title='Subtitle downloaded', display_duration_in_ms=3000, fade_in_duration=100)
                else:
                    sg.popup_ok('There was an error in dowloading file, please try again')

            window_download_subs['MOVIENAME'].update(movie.title)
            window_download_subs['MOVIEYEAR'].update(movie.year)
            window_download_subs['IMDBID'].update(movie.imdb_id)
            window_download_subs['KIND'].update(movie.kind)
            sub_name = []
            for q in range(len(all_subs)):
                sub_name.append(all_subs[q].MovieReleaseName)
            window_download_subs['SUBSTABLE'].update(values=sub_name)
            
    window.close() # Closes main window
    return