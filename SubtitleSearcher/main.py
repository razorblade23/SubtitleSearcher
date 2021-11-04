'''
    Before running this as python script you must install python3 and a good idea is to make a virtual enviroment.
    Virtual enviroment is often called venv. As of python 3.6 venv is automaticly included in python installation.

    Create empty folder in terminal and enter it.

    For Windows activation:
    -> python -m venv venv/
    -> venv/Scripts/activate.ps1 (for PowerShell terminal)
    -> venv/Scripts/activate.bat (for CMD terminal)
    For Linux activation:
    -> python3 -m venv venv/.
    -> source venv/bin/activate

    When you are in your activated virtual enviroment (there is a name of your env in parenthesis () before command in terminal) run:
    pip install -r requirements.txt

    This will install all the modules needed for this to work
'''
# Importing modules
import os
import PySimpleGUI as sg
from tkinter.constants import FALSE
from SubtitleSearcher.data import handle_zip
from SubtitleSearcher import gui_control, gui_windows
import platform

system = platform.system()
if system == 'Windows':
    icon = 'SubtitleSearcher/static/images/image.ico'
if system == 'Linux':
    icon = 'SubtitleSearcher/static/images/image.png'

WINDOWSUBS = False
language_selected = []

main_layout = gui_windows.main_window()
single_sub_layout = gui_windows.subs_window()

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

        if event == 'Save':
            if values['KeepOnTop'] == False:
                window.keep_on_top_clear()
            else:
                window.keep_on_top_set()

        if event == 'SEARCHBYSINGLEFILE':
            language_selected = gui_control.language_selector(values)
            lang = language_selected[0]
            movie, all_subs = gui_control.search_by_single_file(values, lang)

        if not WINDOWSUBS and event == 'SEARCHBYSINGLEFILE':
            WINDOWSUBS = True
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
                    if sub.sub_file_name == values_subs['SUBSTABLE'][0]:
                        sub_selected_filename = sub.sub_file_name
                        sub_selected_lang = sub.sub_lang_id
                        sub_selected_score = sub.score
                        sub_selected_zip_down = sub.sub_zip_donwload_link
                window_download_subs['SUBNAME'].update(sub_selected_filename)
                window_download_subs['SUBLANG'].update(sub_selected_lang)
                window_download_subs['SUBSCORE'].update(sub_selected_score)
                window_download_subs['DOWNLOADSUB'].update(disabled=False)

            if event_subs == 'DOWNLOADSUB':
                selected_sub = handle_zip.ZipHandler(sub_selected_filename, sub_selected_zip_down, values['SINGLEFILE'])
                downloadIt = selected_sub.download_zip()
                if downloadIt:
                    sg.popup_ok('File downloaded succesfully.', title='Success')
                    selected_sub.extract_zip()
                    selected_sub.move_files()
                else:
                    sg.popup_ok('There was an error in dowloading file, please try again')

            window_download_subs['MOVIENAME'].update(movie.name)
            window_download_subs['MOVIEYEAR'].update(movie.year)
            window_download_subs['IMDBID'].update(movie.imdb_id)
            sub_name = []
            for q in range(len(all_subs)):
                sub_name.append(all_subs[q].sub_file_name)
            window_download_subs['SUBSTABLE'].update(values=sub_name)
            

    #os.system('clear') # Clears terminal window
    window.close() # Closes main window
    return