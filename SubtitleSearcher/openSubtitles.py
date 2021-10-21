from bs4 import BeautifulSoup
import requests

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