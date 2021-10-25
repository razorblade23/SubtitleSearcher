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
from SubtitleSearcher import openSubtitles
from SubtitleSearcher import imdb_metadata
#from SubtitleSearcher.static.images.base64_img import icon
import PySimpleGUI as sg
import platform

system = platform.system()
if system == 'Windows':
    icon = 'SubtitleSearcher/static/images/image.ico'
if system == 'Linux':
    icon = 'SubtitleSearcher/static/images/image.png'

sg.theme('DarkBrown4')

layout = [
    [sg.Image(source='SubtitleSearcher/static/images/logo.png')],
    [sg.Text('Project aiming to make finding and downloading subtitles a breeze!', font='Any 16')],
    [sg.TabGroup(layout=[
        [sg.Tab(title='Main', layout=[
            [sg.Frame(title='Search for subtitles', layout=[
                [sg.TabGroup(layout=[
                    [sg.Tab(title='Search by file', layout=[
                        [sg.InputText(disabled=True, key='SINGLEFILE', default_text='Browse this to select a single file !'), sg.FileBrowse('Browse', size=(8,2), key='ChooseSingle', file_types=(('Video files', '.avi'),('Video files', '.mkv'),))], 
                        [sg.InputText(disabled=True, key='MULTIPLEFILES', default_text='Browse this to select multiple files !'), sg.FilesBrowse('Browse', size=(8,2), key='ChooseMultiple', file_types=(('Video files', '.avi'),('Video files', '.mkv'),))],
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
            [sg.Checkbox('Use opensubtitles.org?', key='UseOPENSUBTITLES')],
            [sg.Text('You must input your opensubtitles account information !')],
            [sg.InputText('Username', key='openUSERNAME')],
            [sg.InputText('Password', key='openPASS')]
        ])]
    ])]
]

window = sg.Window(title='Subby doo', layout=layout, element_justification='center', icon=icon, finalize=True)


while True:
    event, values = window.read(timeout=400)
    if event == sg.WIN_CLOSED:
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
    if event == 'SEARCHONIMDB':
        _dict = imdb_metadata.search_by_id(values['IMDBID'])
        window['MovieTitle'].update(value=_dict['resource']['title'])
        window['MovieYear'].update(value=_dict['resource']['year'])
    
    if event == 'SEARCHBYSINGLEFILE':
        hashed_file = openSubtitles.hashFile(values['SINGLEFILE'])
        print(hashed_file)
