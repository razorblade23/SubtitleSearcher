import requests

api_url = 'https://kodi.titlovi.com/api/subtitles'


class TitloviCom:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.search_param = {}
        self.LANGUAGE_MAPPING = {
                                'eng': 'English',
                                'hrv': 'Hrvatski',
                                'scc': 'Srpski',
                                'slv': 'Slovenski',
                                'Macedonian': 'Makedonski',
                                'bos': 'Bosanski'
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
                return resp_json
            elif response.status_code == requests.codes.unauthorized:
                return None
            else:
                return None
        except Exception as e:
            return None
    
    def set_user_login_details(self):
        login = self.handle_login()
        self.user_token = login['Token']
        self.token_expiry_date = login['ExpirationDate']
        self.user_id = login['UserId']
    
    def search_by_filename(self, movie_name, year):
        self.set_user_login_details()
        self.search_param['query'] = movie_name
        self.search_param['year'] = year
    
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