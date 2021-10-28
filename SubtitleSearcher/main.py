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
from SubtitleSearcher.data import openSubtitles, movies
import PySimpleGUI as sg
import platform
import urllib.parse

system = platform.system()
if system == 'Windows':
    icon = 'SubtitleSearcher/static/images/image.ico'
if system == 'Linux':
    icon = 'SubtitleSearcher/static/images/image.png'



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
                [sg.Checkbox('English', key='LangENG'), sg.Checkbox('Croatian', key='LangCRO'), sg.Checkbox('Serbian', key='LangSRB'), sg.Checkbox('Bosnian', key='LangBOS'), sg.Checkbox('Slovenian', key='LangSLO')]
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
                [sg.T(key='MOVIENAME', text_color='white')]
            ]),
            sg.Column(layout=[
                [sg.T('Movie year:')],
                [sg.T(key='MOVIEYEAR', text_color='white')]
            ]),
            sg.Column(layout=[
                [sg.T('Movie IMDB ID:')],
                [sg.T(key='IMDBID', text_color='white')]
            ])],
        ])],
        [sg.Frame(title='Select subtitle', layout=[
            [sg.Table(values=[['','','']], headings=['#', 'Subtitle name', 'Subtitle language'], auto_size_columns=True, key='SUBSTABLE')]
        ]),
        sg.Frame(title='Selected file metadata', layout=[
            [sg.Column(layout=[
                [sg.T('Subtitle name:')],
                [sg.T(key='SUBNAME', text_color='white')]
            ])],
            [sg.Column(layout=[
                [sg.T('Subtitle language:')],
                [sg.T(key='SUBLANG', text_color='white')]
            ])],
            [sg.Column(layout=[
                [sg.T('Subtitle score:')],
                [sg.T(key='SUBSCORE', text_color='white')]
            ])],
        ])]
    ]
    return layout

sg.theme('DarkBrown4')



# Start infinite loop for your GUI windows and reading from them
def run():
    WINDOWSUBS = False
    window = sg.Window(title='Subbydoo', layout=main_window(), element_justification='center', icon=icon, finalize=True)
    while True:
        event, values = window.read(timeout=400) # This window.read() is how you get all values and events from your windows
        if event == sg.WIN_CLOSED: # If window is closed break from the loop
            break
        if event == 'Save':
            if values['KeepOnTop'] == False:
                window.keep_on_top_clear()
            else:
                window.keep_on_top_set()
        if event == 'SEARCHBYIMDB':
            language_selected = []
            if values['LangENG']:
                language_selected.append('eng')
            elif values['LangCRO']:
                language_selected.append('hrv')
            elif values['LangSRB']:
                language_selected.append('srb')
            elif values['LangBOS']:
                language_selected.append('bos')
            else:
                sg.popup_ok('Language is not selected')
                continue
            subtitles_dict = print(openSubtitles.search_by_imdb(values['IMDBID'], language_selected[0]))
        #if event == 'SEARCHONIMDB':
        #    _dict = imdb_metadata.search_by_id(values['IMDBID'])
        #    window['MovieTitle'].update(value=_dict['resource']['title'])
        #    window['MovieYear'].update(value=_dict['resource']['year'])
        
        if event == 'SEARCHBYSINGLEFILE':
            opensubs = openSubtitles.searchOpenSubtitles()
            try:
                hashed_file = opensubs.hashFile(values['SINGLEFILE'])
                fileSize = opensubs.sizeOfFile(values['SINGLEFILE'])
            except FileNotFoundError:
                sg.popup_ok('File not found, please try again', title='File not found')
                continue
            else:
                movie = movies.Movie(fileSize, hashed_file)
                link = opensubs.create_link(bytesize=fileSize, hash=hashed_file, language='hrv')
                subtitles = opensubs.request_subtitles(link)
            subtitles = []
            all_subs = []
            if len(subtitles) == 0: # If finding movie with hash failed and list "subtitles" is empty so it len
                movie_name = sg.popup_get_text('Finding subtitles using hash failed!\nPlease input name of your movie.')
                movie_name.lower()
                movie_name = urllib.parse.quote(movie_name)
                link = opensubs.create_link(query=movie_name, language='hrv')
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
            print('Total numbers of subtitles found for this entry: {}'.format(len(all_subs)))
            print('Score of a subtitle is used to determine how well it will fit for your movie')
            print('This is first five matching subtitles')
            for i in range(len(all_subs)):
                print()
                print('Score for first subtitle in list: {}'.format(all_subs[i].score))
                print('Use this link to download first in the list in GZ format:\n{}'.format(all_subs[i].sub_download_link))
                print('Use this link to download first in the list in ZIP format:\n{}'.format(all_subs[i].sub_zip_donwload_link))
            WINDOWSUBS = True
        if WINDOWSUBS:
            WINDOWSUBS = False
            window_download_subs = sg.Window(title='Subbydoo - download subs', layout=subs_window(), element_justification='center', icon=icon, finalize=True)
            event_subs, values_subs = window_download_subs.read(timeout=400)
            try:
                window_download_subs['MOVIENAME'].update(movie.name)
                window_download_subs['MOVIEYEAR'].update(movie.year)
                window_download_subs['IMDBID'].update(movie.imdb_id)
            except:
                pass

    os.system('clear') # Clears terminal window
    window.close() # Closes main window