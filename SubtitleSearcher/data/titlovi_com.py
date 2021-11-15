import requests

api_url = 'https://kodi.titlovi.com/api/subtitles'


class TitloviCom:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.search_param = {}

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
        self.search_API()
    
    def search_API(self):
        self.search_param['lang'] = 'Hrvatski'
        self.search_param['token'] = self.user_token
        self.search_param['userid'] = self.user_id
        self.search_param['json'] = True
        response = requests.get('{0}/search'.format(api_url), params=self.search_param)
        if response.status_code == requests.codes.ok:
                    resp_json = response.json()
        print(resp_json)

    



titlovi = TitloviCom('razorblade23', 'MojeKarlovacko@23')
titlovi.search_by_filename('avatar', 2009)