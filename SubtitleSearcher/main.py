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
from tkinter.constants import FALSE
from SubtitleSearcher.data import openSubtitles, movies, handle_zip
import PySimpleGUI as sg
import platform
import urllib.parse

system = platform.system()
if system == 'Windows':
    icon = 'SubtitleSearcher/static/images/image.ico'
if system == 'Linux':
    icon = 'SubtitleSearcher/static/images/image.png'

WINDOWSUBS = False
language_selected = []

def main_window():
    layout = [
        [sg.Image(source='SubtitleSearcher/static/images/logo.png')],
        [sg.Text('Project aiming to make finding and downloading subtitles a breeze!', font='Any 16')],
        [sg.TabGroup(layout=[
            [sg.Tab(title='Main', layout=[
                [sg.Frame(title='Search for subtitles', layout=[
                    [sg.TabGroup(layout=[
                        [sg.Tab(title='Search by file', layout=[
                            [sg.InputText(disabled=True, key='SINGLEFILE', 
                                            default_text='Browse this to select a single file !', 
                                            disabled_readonly_text_color='red'), 
                                sg.FileBrowse('Browse', size=(8,2), initial_folder='~/Downloads', key='ChooseSingle', 
                                                file_types=(('Video files', '.avi'),('Video files', '.mkv'),))], 
                            [sg.InputText(disabled=True, key='MULTIPLEFILES', default_text='Browse this to select multiple files !', 
                                            disabled_readonly_text_color='red'), 
                            sg.FilesBrowse('Browse', size=(8,2), key='ChooseMultiple', initial_folder='~/Downloads',
                                            file_types=(('Video files', '.avi'),('Video files', '.mkv'),))],
                            [sg.Button('Search for single file', key='SEARCHBYSINGLEFILE'), sg.Button('Search multiple files', key='SEARCHBYMULTIFILE')]
                        ])],
                        [sg.Tab(title='Search by IMDB ID', layout=[
                            [sg.Frame(title='ID', layout=[
                                [sg.Text('Enter IMDB ID')],
                                [sg.InputText(key='IMDBID', size=(8,1))],
                                [sg.Button('Search for movie subtitles', key='SEARCHBYIMDB', disabled=False), sg.Button('Search for movie on IMDB', key='SEARCHONIMDB')]
                            ]), sg.Frame(title='Rezultat', layout=[
                                [sg.Text('', key='MovieTitle')],
                                [sg.Text('', key='MovieYear')]
                            ])]
                        ])]
                    ])]
            ]),
                sg.Frame(title='Select options', layout=[
                    [sg.Checkbox('Use opensubtitles.org ?', key='USEOPEN')],
                    [sg.Checkbox('Use titlovi.com ?', disabled=True)],
                    [sg.Checkbox('Use podnapisi.net ?', disabled=True)],
                    [sg.Checkbox('Use openSubtitles ?', disabled=True)],
                    [sg.Frame(title='Additional settings', layout=[
                        [sg.Checkbox('Keep on top ?', key='KeepOnTop')]
                    ])],
                    [sg.Button('Save', key='Save')]
        ])]
            ])],
            [sg.Tab(title='Languages', layout=[
                [sg.Text('Choose a language for search', font='Any 14')],
                [sg.Radio('Croatian', key='LangCRO', default=True, group_id=1), sg.Radio('English', key='LangENG', group_id=1), sg.Radio('Serbian', key='LangSRB', group_id=1), sg.Radio('Bosnian', key='LangBOS', group_id=1), sg.Radio('Slovenian', key='LangSLO', group_id=1)]
            ])],
            [sg.Tab(title='openSubtitles', layout=[
                [sg.Text('You must input your opensubtitles account information !')],
                [sg.InputText('Username', key='openUSERNAME')],
                [sg.InputText('Password', key='openPASS')]
            ])]
        ])]
    ]
    return layout

def subs_window():
    layout = [
        [sg.Frame(title='Options', layout=[
            [sg.Checkbox('Match subtitle filename with movie filename?'), sg.Checkbox('Append language code to end of subtitle file?')]
        ])],
        [sg.Frame(title='Selected movie metadata', layout=[
            [sg.Column(layout=[
                [sg.T('Movie name:')],
                [sg.T(key='MOVIENAME', text_color='white', size=(30,1))]
            ]),
            sg.Column(layout=[
                [sg.T('Movie year:')],
                [sg.T(key='MOVIEYEAR', text_color='white', size=(5,1))]
            ]),
            sg.Column(layout=[
                [sg.T('Movie IMDB ID:')],
                [sg.T(key='IMDBID', text_color='white', size=(8,1))]
            ])],
        ])],
        [sg.Frame(title='Select subtitle', layout=[
            [sg.Listbox(values=[['1','2','3'],['4','4','4']], key='SUBSTABLE', size=(80,20), select_mode='LISTBOX_SELECT_MODE_SINGLE', enable_events=True)]
        ]),
        sg.Frame(title='Selected file metadata', layout=[
            [sg.Column(layout=[
                [sg.T('Subtitle name:')],
                [sg.T(key='SUBNAME', text_color='white', size=(65,1))]
            ])],
            [sg.Column(layout=[
                [sg.T('Subtitle language:')],
                [sg.T(key='SUBLANG', text_color='white', size=(10,1))]
            ])],
            [sg.Column(layout=[
                [sg.T('Subtitle score:')],
                [sg.T(key='SUBSCORE', text_color='white', size=(10,1))]
            ])],
        ])],
        [sg.Button('Download', key='DOWNLOADSUB', disabled=True)]
    ]
    return layout

sg.theme('DarkBrown4')

# Start infinite loop for your GUI windows and reading from them
def run():
    global WINDOWSUBS, language_selected
    window = sg.Window(title='Subbydoo', layout=main_window(), element_justification='center', icon=icon, finalize=True)
    while True:
        event, values = window.read(timeout=400) # This window.read() is how you get all values and events from your windows
        #print(f'Event: {event}')
        #print(f'Values: {values}')
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
            pass

        if event == sg.WIN_CLOSED: # If window is closed break from the loop
            break
        if event == 'Save':
            if values['KeepOnTop'] == False:
                window.keep_on_top_clear()
            else:
                window.keep_on_top_set()
        if event == 'SEARCHBYSINGLEFILE':
            lang = language_selected[0]
            opensubs = openSubtitles.searchOpenSubtitles()
            try:
                hashed_file = opensubs.hashFile(values['SINGLEFILE'])
                fileSize = opensubs.sizeOfFile(values['SINGLEFILE'])
            except FileNotFoundError:
                sg.popup_ok('File not found, please try again', title='File not found')
                continue
            else:
                movie = movies.Movie(fileSize, hashed_file)
                link = opensubs.create_link(bytesize=fileSize, hash=hashed_file, language=lang)
                subtitles = opensubs.request_subtitles(link)
            #subtitles=[] # Comment / Uncomment this to simulate finding hash failed
            all_subs = []
            if len(subtitles) == 0: # If finding movie with hash failed and list "subtitles" is empty so it length is 0 
                movie_name = sg.popup_get_text('Finding subtitles using hash failed!\nPlease input name of your movie.')
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
                    #sub = movies.MovieSubtitle(number, subtitle['SubFileName'], subtitle['SubLanguageID'], subtitle['SubFormat'], subtitle['SubDownloadsCnt'], subtitle['SubDownloadLink'], subtitle['ZipDownloadLink'], subtitle['Score'])
                    if number == 0:
                        movie.set_metadata(subtitle['MovieName'], subtitle['MovieYear'], subtitle['SubDownloadLink'], subtitle['ZipDownloadLink'], subtitle['IDMovieImdb'])
                    number = movies.MovieSubtitle(subtitle['SubFileName'], subtitle['SubLanguageID'], subtitle['SubFormat'], subtitle['SubDownloadsCnt'], subtitle['SubDownloadLink'], subtitle['ZipDownloadLink'], subtitle['Score'])
                    all_subs.append(number)
            #print('Total numbers of subtitles found for this entry: {}'.format(len(all_subs)))
            #print('Score of a subtitle is used to determine how well it will fit for your movie')
            #print('Here are first 10 matching subtitles')
            #for i in range(len(all_subs)):
            #    if i >= 10:
            #        continue
            #    print()
            #    print('Subtitle number: {}'.format(i+1))
            #    print('Subtitle name:\n{}'.format(all_subs[i].sub_file_name))
            #    print('Subtitle downloads count: {}'.format(all_subs[i].sub_download_count))
            #    print('Score: {}'.format(all_subs[i].score))
            #    print('Use this link to download in GZ format:\n{}'.format(all_subs[i].sub_download_link))
            #    print('Use this link to download in ZIP format:\n{}'.format(all_subs[i].sub_zip_donwload_link))
        if not WINDOWSUBS and event == 'SEARCHBYSINGLEFILE':
            WINDOWSUBS = True
            layout_select_subs = subs_window()
            window_download_subs = sg.Window(title='Subbydoo - download subs', layout=layout_select_subs, element_justification='center', icon=icon, finalize=True)
        if WINDOWSUBS:
            event_subs, values_subs = window_download_subs.read(timeout=400)
            #print(f'Event: {event_subs}')
            #print(f'Values: {values_subs}')
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