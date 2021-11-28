import requests
import json

API_KEY = 'GJ0Qg0rcBepMq9vUB0NYnbLD9xHAVjpM'
BASE_URL = 'https://api.opensubtitles.com/api/v1/'

class OpenSubtitlesAPI:

    def user_login(self, username, password):
        url = f'{BASE_URL}login'
        payload = {
            'username': username,
            'password': password
        }

        headers = {
            'Content-Type': "application/json",
            'Api-Key': API_KEY
        }
        response = requests.post(url, json=payload, headers=headers)
        respond = False
        if response.ok:
            json_dict = json.loads(response.text)
            self.user_allowed_translations = json_dict['user']['allowed_translations']
            self.user_allowed_downloads = json_dict['user']['allowed_downloads']
            self.user_level = json_dict['user']['level']
            self.user_id = json_dict['user']['user_id']
            self.user_ext_installed = json_dict['user']['ext_installed']
            self.user_vip = json_dict['user']['vip']
            self.user_token = json_dict['token']
            respond = True
            return respond
        else:
            print(f'There was a problem logging user in, error code: {response.status_code}\n{response}')
            respond = False
            return respond
    
    def user_logout(self):
        url = f'{BASE_URL}logout'

        headers = {
            'Content-Type': "application/json",
            'Api-Key': API_KEY
        }
        response = requests.delete(url, headers=headers)
        if response.ok:
            print('User logged out')
        else:
            print(f'There was a problem with logout. response code: {response.status_code}\n{response.text}')

class SearchForSubs(OpenSubtitlesAPI):

    def __init__(self):
        self.ai_translated = 'exclude'  # exclude, include (default: exclude)
        self.episode_number = 0  # for TV shows
        self.foreign_parts_only = 'include'  # exclude, include, only (default: include)
        self.hearing_impaired = 'include'  # include, exclude, only. (default: include)
        self.id = 0  # ID of the movie or episode
        self.imdb_id = 0  # IMDB ID of the movie or episode
        self.languages = ''  # Language code(s), coma separated (en,fr)
        self.machine_translated = 'exclude'  # exclude, include (default: exclude)
        self.moviehash = ''  # Moviehash of the movie (16 characters long)
        self.moviehash_match = 'include'  # include, only (default: include)
        self.order_by = ''  # Order of the returned results, accept any of above fields
        self.order_direction = ''  # Order direction of the returned results (asc,desc)
        self.page = 1
        self.parent_feature_id = 0  # for TV shows
        self.parent_imdb_id = 0  # for TV shows
        self.parent_tmdb_id = 0  # for TV shows
        self.query = ''  # file name or text search
        self.trusted_sources = 'include'  # include, only (default: include)
        self.type = 'all'  # movie, episode or all, (default: all)
        self.user_id = 0  # To be used alone - for user uploads listing
        self.year = 0  # Filter by movie/episode year

    def set_payload(self, **kwargs):
        return kwargs

    def search_subtitles(self, payload):
        url = f'{BASE_URL}subtitles'
        headers = {
            'Content-Type': "application/json",
            'Api-Key': API_KEY
        }
        print(f'sending request using this payload\n{payload}')
        response = requests.get(url, params=payload, headers=headers, allow_redirects=True)
        json_dict = json.loads(response.text)
        json_dict_pretty = json.dumps(json_dict, indent=2)
        self.total_pages = json_dict['total_pages']
        self.total_count = json_dict['total_count']
        self.page = json_dict['page']
        self.data = json_dict['data']

class DownloadSubtitle:
    def download_info(self, file_id):
        url = "https://api.opensubtitles.com/api/v1/download"

        payload = {
            'file_id': file_id
        }
        headers = {
            'Content-Type': "application/json",
            'Api-Key': API_KEY
            }
        response = requests.post(url, data=payload, headers=headers)
        return response.text
        #json_data = json.loads(response.text)
        #self.download_link = json_data['link']
        #self.download_fname = json_data['fname']
        #self.download_requests = json_data['requests']
        #self.download_allowed = json_data['allowed']
        #self.download_remaining = json_data['remaining']
        #self.download_message = json_data['message']



class OpenSubtitlesSubtitleResults:
    def __init__(self, results_data):
        data = results_data
        self.engine = 'OpenSubtitles'
        self.id = data['id']
        self.type = data['type']
        self.attributes = data['attributes']
        self.subtitle_id = data['attributes']['subtitle_id']
        self.language = data['attributes']['language']
        self.download_count = data['attributes']['download_count']
        self.new_download_count = data['attributes']['download_count']
        self.hearing_impaired = data['attributes']['hearing_impaired']
        self.hd = data['attributes']['hd']
        self.fps = data['attributes']['fps']
        self.votes = data['attributes']['votes']
        self.ratings = data['attributes']['ratings']
        self.from_trusted = data['attributes']['from_trusted']
        self.foreign_parts_only = data['attributes']['foreign_parts_only']
        self.upload_date = data['attributes']['upload_date']
        self.ai_translated = data['attributes']['ai_translated']
        self.machine_translated = data['attributes']['machine_translated']
        self.release = data['attributes']['release']
        self.comments = data['attributes']['comments']
        self.legacy_subtitle_id = data['attributes']['legacy_subtitle_id']
        self.uploader_id = data['attributes']['uploader']['uploader_id']
        self.uploader_name = data['attributes']['uploader']['name']
        self.uploader_rank = data['attributes']['uploader']['rank']
        self.feature_id = data['attributes']['feature_details']['feature_id']
        self.feature_type = data['attributes']['feature_details']['feature_type']
        self.year = data['attributes']['feature_details']['year']
        self.title = data['attributes']['feature_details']['title']
        self.movie_name = data['attributes']['feature_details']['movie_name']
        self.imdb_id = data['attributes']['feature_details']['imdb_id']
        self.tmdb_id = data['attributes']['feature_details']['tmdb_id']
        self.feature_type = data['attributes']['feature_details']['feature_type']
        self.url = data['attributes']['url']
        self.related_label = data['attributes']['related_links']['label']
        self.related_url = data['attributes']['related_links']['url']
        self.related_img_url = data['attributes']['related_links']['img_url']
        self.file_id = data['attributes']['files'][0]['file_id']
        self.cd_number = data['attributes']['files'][0]['cd_number']
        self.file_name = data['attributes']['files'][0]['file_name']
        self.moviehash_match = data['attributes']['moviehash_match']
        

        

#avatar = SearchForSubs()
#avatar.user_login('smartakus', 'MojeKarlovacko@23')
#
#
#payload = avatar.set_payload(query='Avatar', year=2009, languages='hr')
#avatar.search_subtitles(payload)
#
#print(avatar.data[0])