'''
    Before running this as python script you must install python3 and a good idea is to make a virtual enviroment.
    Virtual enviroment is often called venv. As of python 3.6 venv is automaticly included in python installation.
    
    When you are in your activated virtual enviroment (there is a name of your env in parenthesis () before command in terminal) run:
    pip install -r requirements.txt

    This will install all the modules needed for this to work
'''
# Importing modules
from SubtitleSearcher.openSubtitles import siteSearch
from SubtitleSearcher.static.images import *
import PySimpleGUI as sg

# Setting global variables
opensubtitles_search_url = 'https://www.opensubtitles.org/hr/search2/'
# there will be more of these
# Putting all of sources in the list
sources_list = [opensubtitles_search_url]

def langSelector(language_to_search):
    return 'sublanguageid-{}/'.format(language_to_search)

layout = [
    [sg.Image(data=logo)],
    [sg.Text('Subtitle Search', font='Any 22')],
    [sg.Text('Project aiming to make finding and downloading subtitles a breeze!', font='Any 16')],
    [sg.Column(layout=[
        [sg.Button('Choose a file', size=(30,2))], 
        [sg.Button('Choose a folder', size=(30,2))],
    ]),
    sg.Column(layout=[
        [sg.Text('Choose a language for search', font='Any 14')],
        [sg.Checkbox('English'), sg.Checkbox('Croatian'), sg.Checkbox('Serbian'), sg.Checkbox('Bosnian')]
    ])]
    
]

window = sg.Window(title='SubtitleSearcher', layout=layout, text_justification='center', element_justification='center')



# Video to search first implementation
#video_to_search = sg.popup_get_file('Please choose a video file for subtitle search', 'Choose a file')

openSubtitles = siteSearch(sources_list[0], 'eng')

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break
