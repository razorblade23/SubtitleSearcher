import requests
import json
import urllib
from dateutil import parser
from contextlib import suppress
from SubtitleSearcher.main import log


class OpenSubtitles_API:
    '''This class represents OpenSubtitlesAPI comunnication protocol
    OpenSubtitles gives you user token that should be new every time that you open app
    '''
    def __init__(self):
        self.BASE_URL = 'https://api.opensubtitles.com/api/v1'
        self.API_KEY = 'CIVqd03XEgIT4ERQX0AGlUjcaFCfRdyI'
        
        self.username = None
        self.password = None

        self.user_allowed_translations = None
        self.user_allowed_downloads = None
        self.user_level = None
        self.user_id = None
        self.user_ext_installed = None
        self.user_vip = None
        self.user_token = None
        self.header_basic = {
            'Content-Type': "application/json",
            'Api-Key': self.API_KEY
        }
        self.header_basicAuth = {
            'Content-Type': "application/json",
            'Api-Key': self.API_KEY,
            'Authorization':  self.user_token
        }
        log.debug('Created empty OpenSubtitles_API object')
    
    def set_API_key(self, api_key):
        self.API_KEY = api_key

    def set_user(self, username: str, password: str):
        '''Log the user in
        param: username - username registered on site
        param: password - password registered on site
        '''
        self.username = username
        self.password = password
        log.debug('Username and password set')
    
    def login_user(self):
        url = self.BASE_URL + '/login'
        payload = {
            'username': self.username,
            'password': self.password
        }

        log.info(f'Logging {self.username} in - OpenSubtitles')
        response = requests.post(url, json=payload, headers=self.header_basic)
        return response
    
    def proccess_login_response(self, response):
        if response.ok:
            log.info('User logged in')
            json_dict = json.loads(response.text)
            self.user_allowed_translations = json_dict['user']['allowed_translations']
            self.user_allowed_downloads = json_dict['user']['allowed_downloads']
            self.user_level = json_dict['user']['level']
            self.user_id = json_dict['user']['user_id']
            self.user_ext_installed = json_dict['user']['ext_installed']
            self.user_vip = json_dict['user']['vip']
            self.user_token = json_dict['token']
        else:
            log.warning(f'There was a problem logging user in, error code: {response.status_code} - OpenSubtitles')
    
    def logout_user(self):
        '''Log user out - should be called on program exit'''
        url = self.BASE_URL + '/logout'
        response = requests.delete(url, headers=self.header_basicAuth)
        if response.ok:
            log.info('User logged out')
        else:
            log.warning(f'There was a problem with logout. response code: {response.status_code}')

    @staticmethod
    def prepare_payload(**kwargs):
        return kwargs
    
    @staticmethod
    def prepare_request(payload):
        url_string = urllib.parse.urlencode(payload, safe=',')
        url_string_mod = url_string.replace('+', ' ')
        return url_string_mod
    
    def search_for_subtitle(self, **kwargs):
        url = self.BASE_URL + '/subtitles'
        response = requests.get(url, headers=self.header_basic, params=kwargs, allow_redirects=True)
        return response
    
    def proccess_subtitle_search_response(self, response):
        if response.ok:
            response_dict = json.loads(response.text)
            self.total_pages = response_dict['total_pages']
            self.total_count = response_dict['total_count']
            self.page = response_dict['page']
            self.data = response_dict['data']
        else:
            log.error('There was a problem in proccesing subtitle search response')
            log.error(f'Response returned code {response.status_code}')
            log.error(f'Response returned text {response.text}')
    
    def prepare_download(self, file_id):
        url = self.BASE_URL + '/download'
        payload = {
            'file_id': file_id,
            'sub_format': 'srt'
        }
        response = requests.post(url, json=payload, headers=self.header_basicAuth)
        return response

    def proccess_download_response(self, response):
        data = json.loads(response.text)
        with suppress(KeyError): self.download_link = data['link']
        with suppress(KeyError): self.download_fname = data['fname']
        with suppress(KeyError): self.download_requests = data['requests']
        with suppress(KeyError): self.download_allowed = data['allowed']
        with suppress(KeyError): self.download_remaining = data['remaining']
        with suppress(KeyError): self.download_message = data['message']
    
    @staticmethod
    def download_subtitle(download_link):
        r = requests.get(download_link, allow_redirects=True, timeout=20)
        open('downloaded/subtitle.srt', 'wb').write(r.content)

class ProccessOpenSubtitlesSubs:
    def __init__(self):
        self.engine = 'OpenSubtitles'
        self.id = None
        self.type = None
        self.attributes = None
        self.subtitle_id = None
        self.language = None
        self.download_count = None
        self.new_download_count = None
        self.hearing_impaired = None
        self.hd = None
        self.fps = None
        self.votes = None
        self.ratings = None
        self.from_trusted = None
        self.foreign_parts_only = None
        self.upload_date = None
        self.ai_translated = None
        self.machine_translated = None
        self.release = None
        self.comments = None
        self.legacy_subtitle_id = None
        self.uploader_id = None
        self.uploader_name = None
        self.uploader_rank = None
        self.feature_id = None
        self.feature_type = None
        self.year = None
        self.title = None
        self.movie_name = None
        self.imdb_id = None
        self.tmdb_id = None
        self.feature_type = None
        self.url = None
        self.related_label = None
        self.related_url = None
        self.related_img_url = None
        self.file_id = None
        self.cd_number = None
        self.file_name = None
        self.moviehash_match = None
    
    def make_objects_from_subtitles(self, subtitle):
        self.id = subtitle['id']
        self.type = subtitle['type']
        self.attributes = subtitle['attributes']
        self.subtitle_id = subtitle['attributes']['subtitle_id']
        self.language = subtitle['attributes']['language']
        self.download_count = subtitle['attributes']['download_count']
        self.new_download_count = subtitle['attributes']['download_count']
        self.hearing_impaired = subtitle['attributes']['hearing_impaired']
        self.hd = subtitle['attributes']['hd']
        self.fps = subtitle['attributes']['fps']
        self.votes = subtitle['attributes']['votes']
        self.ratings = subtitle['attributes']['ratings']
        self.from_trusted = subtitle['attributes']['from_trusted']
        self.foreign_parts_only = subtitle['attributes']['foreign_parts_only']
        self.upload_date = subtitle['attributes']['upload_date']
        self.ai_translated = subtitle['attributes']['ai_translated']
        self.machine_translated = subtitle['attributes']['machine_translated']
        self.release = subtitle['attributes']['release']
        self.comments = subtitle['attributes']['comments']
        self.legacy_subtitle_id = subtitle['attributes']['legacy_subtitle_id']
        self.uploader_id = subtitle['attributes']['uploader']['uploader_id']
        self.uploader_name = subtitle['attributes']['uploader']['name']
        self.uploader_rank = subtitle['attributes']['uploader']['rank']
        self.feature_id = subtitle['attributes']['feature_details']['feature_id']
        self.feature_type = subtitle['attributes']['feature_details']['feature_type']
        self.year = subtitle['attributes']['feature_details']['year']
        self.title = subtitle['attributes']['feature_details']['title']
        self.movie_name = subtitle['attributes']['feature_details']['movie_name']
        self.imdb_id = subtitle['attributes']['feature_details']['imdb_id']
        self.tmdb_id = subtitle['attributes']['feature_details']['tmdb_id']
        self.feature_type = subtitle['attributes']['feature_details']['feature_type']
        self.url = subtitle['attributes']['url']
        with suppress(TypeError): self.related_label = subtitle['attributes']['related_links']['label']
        with suppress(TypeError): self.related_url = subtitle['attributes']['related_links']['url']
        with suppress(TypeError): self.related_img_url = subtitle['attributes']['related_links']['img_url']
        self.file_id = subtitle['attributes']['files'][0]['file_id']
        self.cd_number = subtitle['attributes']['files'][0]['cd_number']
        self.file_name = subtitle['attributes']['files'][0]['file_name']
        self.moviehash_match = subtitle['attributes']['moviehash_match']

class Titlovi_API:
    def __init__(self):
        self.BASE_URL = 'https://kodi.titlovi.com/api/subtitles'
        self.username = None
        self.password = None
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
    
    def set_user(self, username, password):
        self.username = username
        self.password = password
        log.info('User set up')
    
    def login_user(self):
        url = self.BASE_URL + '/gettoken'
        param = {
            'username': self.username,
            'password': self.password
        }
        log.info(f'Logging {self.username} in - Titlovi')
        response = requests.post(url, params=param)
        return response
    
    def proccess_login_response(self, response):
        if response.ok:
            data = json.loads(response.text)
            self.user_token = data['Token']
            self.token_expiry_date = parser.isoparse(data['ExpirationDate'])
            self.user_id = data['UserId']
        else:
            log.warning(f'There was a problem and user is not logged in - error code: {response.status_code} - Titlovi')
            if response.status_code == 502:
                log.info('There was a problem with a server, trying again')
                response = self.login_user()
                self.proccess_login_response()

    def handle_language_conversion(self, language: str):
        '''This is needed because we use mapping for OpenSubtitles and that wont work for Titlovi API'''
        languages = language.split(',')
        conv_lang_list = []
        for lang in languages:
            conv_lang = self.LANGUAGE_MAPPING[lang]
            conv_lang_list.append(conv_lang)
        return conv_lang_list
    
    @staticmethod
    def prepare_payload(**kwargs):
        return kwargs

    def search_for_subtitles(self, payload, language):
        url = self.BASE_URL + '/search'
        payload['lang'] = language
        payload['token'] = self.user_token
        payload['userid'] = self.user_id
        payload['json'] = True
        response = requests.get(url, params=payload)
        return response
    
    def proccess_subtitle_search_response(self, response):
        if response.ok:
            date = json.loads(response.text)
            self.results_count = date['ResultsFound']
            self.pages_available = date['PagesAvailable']
            self.current_page = date['CurrentPage']
            self.subtitles = date['SubtitleResults']
        else:
            log.warning(f'There was a problem proccessing response, error code: {response.status_code}')
            log.warning(f'>>>{response.text}')

    @staticmethod
    def download_subtitle(donwload_link):
        r = requests.get(donwload_link, allow_redirects=True, timeout=20)
        open('downloaded/sub.zip', 'wb').write(r.content)

class ProccessTitloviSubs():
    def __init__(self):
        self.engine = 'Titlovi'

    def proccess_subtitle_results(self, subtitle):
        self.id = subtitle['Id']
        self.title = subtitle['Title']
        self.year = subtitle['Year']
        self.type = subtitle['Type']
        self.link = subtitle['Link']
        self.season = subtitle['Season']
        self.episode = subtitle['Episode']
        self.special = subtitle['Special']
        self.lang = subtitle['Lang']
        self.date = subtitle['Date']
        self.downloadCount = subtitle['DownloadCount']
        self.rating = subtitle['Rating']
        self.release = subtitle['Release']


class PersistanceManager(OpenSubtitles_API, Titlovi_API):
    def __init__(self):
        OpenSubtitles_API.__init__(self)
        Titlovi_API.__init__(self)
        self.OpenSubtitlesSettingsPath = 'SubtitleSearcher/data/user_settings/OpenSubtitles_settings.json'
        self.TitloviSettingsPath = 'SubtitleSearcher/data/user_settings/Titlovi_settings.json'
        self.UserSettingsPath = 'SubtitleSearcher/data/user_settings/User_settings.json'

    def save_userdata(self, location, **kwargs):
        if location == 'OpenSubtitles':
            with open(self.OpenSubtitlesSettingsPath, 'w') as file:
                json.dump(kwargs, file)
        if location == 'Titlovi':
            with open(self.TitloviSettingsPath, 'w') as file:
                json.dump(kwargs, file)
        if location == 'User':
            with open(self.UserSettingsPath, 'w') as file:
                json.dump(kwargs, file)
    
    def load_userdata(self, location):
        if location == 'OpenSubtitles':
            with open(self.OpenSubtitlesSettingsPath, 'r') as file:
                settings = file.read()
                settings_dict = json.loads(settings)
            return settings_dict

        if location == 'Titlovi':
            with open(self.TitloviSettingsPath, 'r') as file:
                settings = file.read()
                settings_dict = json.loads(settings)
            return settings_dict

        if location == 'User':
            with open(self.UserSettingsPath, 'r') as file:
                settings = file.read()
                settings_dict = json.loads(settings)
            return settings_dict



