
from dateutil import parser

from datetime import datetime
import requests
import json
api_url = 'https://kodi.titlovi.com/api/subtitles'


class TitloviCom:
    def __init__(self):
        self.engine = 'Titlovi'
        self.username = None
        self.password = None
        self.search_param = {}
        self.LANGUAGE_MAPPING = {
                                'en': 'English',
                                'hr': 'Hrvatski',
                                'sr': 'Srpski',
                                'sl': 'Slovenski',
                                'Macedonian': 'Makedonski',
                                'bs': 'Bosanski'
        }
        self.user_token = None
        self.token_expiry_date = None
        self.user_id = None

    def handle_login(self):
        """
        Method used for sending user login request.

        OK return:
            {
                "ExpirationDate": datetime string (format: '%Y-%m-%dT%H:%M:%S.%f'),
                "Token": string,
                "UserId": integer,
                "UserName": string
            }

        Error return: None
        """
        login_params = dict(username=self.username, password=self.password, json=True)
        try:
            response = requests.post('{0}/gettoken'.format(api_url), params=login_params)
            if response.status_code == requests.codes.ok:
                resp_json = response.json()
                self.user_token = resp_json['Token']
                self.token_expiry_date = resp_json['ExpirationDate']
                self.user_id = resp_json['UserId']
                return resp_json
            elif response.status_code == requests.codes.unauthorized:
                print(response.status_code)
                return None
            else:
                print(response.status_code)
                return None
        except Exception as e:
            return None
    
    def set_user_login_details(self, login):
        self.user_token = login['Token']
        self.token_expiry_date = login['ExpirationDate']
        self.user_id = login['UserId']
    
    def set_from_json(self, token, userID, expiry_date):
        self.user_token = token
        self.token_expiry_date = expiry_date
        self.user_id = userID
    
    def check_for_expiry_date(self):
        datetime_now = datetime.now()
        parsed_date = parser.isoparse(self.token_expiry_date)
        #token_expiry = datetime.fromisoformat(self.token_expiry_date)
        self.time_left = parsed_date - datetime_now
        time_left = self.time_left.total_seconds()
        days_left = self.time_left.days
        expired = False
        if time_left <= 0:
            expired = True
        return expired, days_left
        
    def search_by_filename(self, movie_name, year, season=None, episode=None, imdb_id=None):
        self.search_param['query'] = movie_name
        self.search_param['year'] = year
        self.search_param['season'] = season
        self.search_param['episode'] = episode
        self.search_param['imdbID'] = imdb_id
    
    def set_language(self, language):
        lang = self.LANGUAGE_MAPPING[language]
        self.search_param['lang'] = lang

    def search_API(self):
        self.search_param['token'] = self.user_token
        self.search_param['userid'] = self.user_id
        self.search_param['json'] = True
        response = requests.get('{0}/search'.format(api_url), params=self.search_param)
        if response.status_code == requests.codes.ok:
                    resp_json = response.json()
        self.results_count = resp_json['ResultsFound']
        self.pages_available = resp_json['PagesAvailable']
        self.current_page = resp_json['CurrentPage']
        self.subtitles = resp_json['SubtitleResults']