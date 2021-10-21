'''
    Before running this as python script you must install python3 and a good idea is to make a virtual enviroment.
    Virtual enviroment is often called venv. As of python 3.6 venv is automaticly included in python installation.
    
    When you are in your activated virtual enviroment (there is a name of your env in parenthesis () before command in terminal) run:
    pip install -r requirements.txt

    This will install all the modules needed for this to work
'''
# Importing modules
import PySimpleGUI as sg
from bs4 import BeautifulSoup
import requests

# Setting global variables
opensubtitles_search_url = 'https://www.opensubtitles.org/hr/search2/'
# there will be more of these
# Putting all of sources in the list
sources_list = [opensubtitles_search_url]

def langSelector(language_to_search):
    return 'sublanguageid-{}/'.format(language_to_search)


# Making a class which will spawn children for specific sites
class siteSearch():
    # This special method __init__ is a contructor.
    def __init__(self, site_to_search, language_to_search):
        self.site_to_search = site_to_search
        self.lang = language_to_search

    def get_user_input(self):
        self.user_input = input('Please enter name and year of the movie: \n')
        self.user_input.replace(' ', '+')
        return self.user_input
    
    def get_url(self, search_string):

        self.response = requests.get('{}sublanguageid-{}/moviename-{}'.format(self.site_to_search, self.lang, search_string))
        return self.response.text
    
    def soupify(self, html_to_parse):
        soup = BeautifulSoup(html_to_parse, 'html.parser')
        find_a = soup.find_all('table')
        tag_name_list = []
        for tag in find_a:
            tag_name_list.append(tag.text)
        return tag_name_list

    def parse_for_titles(self):
        pass

    def run(self):
        user_input = self.get_user_input()
        url_to_parse = self.get_url(user_input)
        soup = self.soupify(url_to_parse)
        return soup

# Video to search first implementation
#video_to_search = sg.popup_get_file('Please choose a video file for subtitle search', 'Choose a file')

openSubtitles = siteSearch(sources_list[0], 'eng')

print(openSubtitles.run())
