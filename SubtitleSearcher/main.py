# Importing modules
import os
import PySimpleGUI as sg
from tkinter.constants import FALSE
from SubtitleSearcher.data import handle_zip
from SubtitleSearcher import gui_control, gui_windows
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


# Start infinite loop for your GUI windows and reading from them
def run():
    global WINDOWSUBS, language_selected
    window = sg.Window(title='Subbydoo', layout=main_layout, element_justification='center', icon=icon, finalize=True)
    while True:
        event, values = window.read(timeout=400) # This window.read() is how you get all values and events from your windows
        #print(f'Event: {event}')
        #print(f'Values: {values}')

        if event == sg.WIN_CLOSED: # If window is closed break from the loop
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

        if not WINDOWSUBS and event == 'SEARCHBYSINGLEFILE':
            WINDOWSUBS = True
            single_sub_layout = gui_windows.subs_window()
            window_download_subs = sg.Window(title='Subbydoo - download subs', layout=single_sub_layout, element_justification='center', icon=icon, finalize=True)
        
        if WINDOWSUBS:
            event_subs, values_subs = window_download_subs.read(timeout=400)
            #print(f'Event: {event_subs}')
            #print(f'Values: {values_subs}')
            window_download_subs['STATUSBAR'].update(value='Subtitles found: {} | Language selected: {}'.format(len(all_subs), language_selected[0]))
            
            if event_subs == sg.WIN_CLOSED:
                WINDOWSUBS = False
                window_download_subs.close()
                continue

            if event_subs == 'SUBSTABLE':
                for sub in all_subs:
                    if sub.SubFileName == values_subs['SUBSTABLE'][0]:
                        window_download_subs['SUBNAME'].update(sub.SubFileName)
                        window_download_subs['SUBSIZE'].update(sub.SubSize)
                        window_download_subs['SUBHASH'].update(sub.SubHash)
                        window_download_subs['SUBUSERID'].update(sub.UserID)
                        window_download_subs['SUBUSERNICK'].update(sub.UserNickName)
                        window_download_subs['SUBADDDATE'].update(sub.SubAddDate)

                        window_download_subs['SUBEXTENSION'].update(sub.SubFormat)
                        window_download_subs['SUBLANG'].update(sub.LanguageName)
                        window_download_subs['SUBDOWNCOUNT'].update(str(sub.SubDownloadsCnt) + ' times')
                        window_download_subs['SUBSCORE'].update(str(sub.Score) + ' %')
                window_download_subs['DOWNLOADSUB'].update(disabled=False)

            if event_subs == 'DOWNLOADSUB':
                sg.popup_notify('Started download of selected subtitle', title='SubbyDoo')
                selected_sub = handle_zip.ZipHandler(sub_selected_filename, sub_selected_zip_down, values['SINGLEFILE'])
                downloadIt = selected_sub.download_zip()
                if downloadIt:
                    sg.popup_ok('File downloaded succesfully.\nYou can find your subtitle in movie folder', title='Success', no_titlebar=True)
                    selected_sub.extract_zip()
                    selected_sub.move_files()
                    selected_sub.delete_remains()
                else:
                    sg.popup_ok('There was an error in dowloading file, please try again')

            window_download_subs['MOVIENAME'].update(movie.title)
            window_download_subs['MOVIEYEAR'].update(movie.year)
            window_download_subs['IMDBID'].update(movie.imdb_id)
            window_download_subs['KIND'].update(movie.kind)
            sub_name = []
            for q in range(len(all_subs)):
                sub_name.append(all_subs[q].SubFileName)
            window_download_subs['SUBSTABLE'].update(values=sub_name)
            

    os.system('clear') # Clears terminal window
    window.close() # Closes main window
    return