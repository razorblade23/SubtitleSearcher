'''
    Before running this as python script you must install python3 and a good idea is to make a virtual enviroment.
    Virtual enviroment is often called venv. As of python 3.6 venv is automaticly included in python installation.
    
    When you are in your activated virtual enviroment (there is a name of your env in parenthesis () before command in terminal) run:
    pip install -r requirements.txt

    This will install all the modules needed for this to work
'''
# Importing modules
from SubtitleSearcher.openSubtitles import siteSearch
import PySimpleGUI as sg

# Setting global variables
opensubtitles_search_url = 'https://www.opensubtitles.org/hr/search2/'
# there will be more of these
# Putting all of sources in the list
sources_list = [opensubtitles_search_url]

def langSelector(language_to_search):
    return 'sublanguageid-{}/'.format(language_to_search)

layout = [
    [sg.Text('Subtitle Search', justification='center')],
    [sg.Text('Project aiming to make finding and downloading subtitles a breeze!', justification='center')]
]

window = sg.Window(title='SubtitleSearcher', layout=layout)



# Video to search first implementation
#video_to_search = sg.popup_get_file('Please choose a video file for subtitle search', 'Choose a file')

openSubtitles = siteSearch(sources_list[0], 'eng')

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break
