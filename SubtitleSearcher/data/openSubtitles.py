import requests
import struct, os
import json

main_search_url = 'https://rest.opensubtitles.org/search/'
headers = {'user-agent': 'TemporaryUserAgent'}

def search_by_imdb(imdb_id, language_code='eng'):
    request = requests.get('{}imdbid-{}/sublanguageid-{}'.format(main_search_url, imdb_id, language_code), headers=headers)
    json_req = json.loads(request.text)
    return json_req

class searchOpenSubtitles:
    def __init__(self):
        self.base_url = 'https://rest.opensubtitles.org/search'
        self.http_header = {'user-agent': 'TemporaryUserAgent'}
        self.episode = 'episode-'
        self.imdb = 'imdbid-'
        self.query = 'query-'
        self.bytesize = 'moviebytesize-'
        self.hash = 'moviehash-'
        self.season = 'season-'
        self.language = 'sublanguageid-'

    def create_link(self, episode=None, imdb=None, query=None, bytesize=None, hash=None, season=None, language=None):
        self.link_text = f'{self.base_url}'
        if episode != None:
            episode_str = f'/{self.episode}{episode}'
            self.link_text = self.link_text + episode_str
        if imdb != None:
            imdb_str = f'/{self.imdb}{imdb}'
            self.link_text = self.link_text + imdb_str
        if query != None:
            query_string = f'/{self.query}{query}'
            self.link_text = self.link_text + query_string
        if bytesize != None:
            bytesize_str = f'/{self.bytesize}{bytesize}'
            self.link_text = self.link_text + bytesize_str
        if hash != None:
            hash_str = f'/{self.hash}{hash}'
            self.link_text = self.link_text + hash_str
        if season != None:
            season_str = f'/{self.season}{season}'
            self.link_text = self.link_text + season_str
        if language != None:
            language_str = f'/{self.language}{language}'
            self.link_text = self.link_text + language_str
        return self.link_text
    
    def request_subtitles(self, link):
        response = requests.get(link, headers=self.http_header)
        json_req = json.loads(response.text)
        return json_req
    
    @staticmethod
    def make_search_string(title, year, quality, resolution, encoder, excess):
        string_list = []
        if not title == None:
            string_list.append(str(title))
        if not year == None:
            string_list.append(str(year))
        if not quality == None:
            string_list.append(str(quality))
        if not resolution == None:
            string_list.append(str(resolution))
        if not encoder == None or not encoder == 1 or not encoder == '1':
            string_list.append(str(encoder))
        if not excess == None:
            string_list.append(str(excess))
        string = ' '.join(string_list)
        print(string)
        return string.lower()
        
    @staticmethod
    def sizeOfFile(name):
        size = os.path.getsize(name)
        return size

    @staticmethod
    def hashFile(name):
        try: 
            longlongformat = '<q'  # little-endian long long
            bytesize = struct.calcsize(longlongformat) 
                
            f = open(name, "rb") 
                
            filesize = os.path.getsize(name) 
            hash = filesize 
                
            if filesize < 65536 * 2: 
                return "SizeError" 
                
            for x in range(int(65536/bytesize)):
                buffer = f.read(bytesize)
                (l_value,)= struct.unpack(longlongformat, buffer)
                hash += l_value
                hash = hash & 0xFFFFFFFFFFFFFFFF #to remain as 64bit number
                        

            f.seek(max(0,filesize-65536),0) 
            for x in range(int(65536/bytesize)): 
                buffer = f.read(bytesize) 
                (l_value,)= struct.unpack(longlongformat, buffer)  
                hash += l_value 
                hash = hash & 0xFFFFFFFFFFFFFFFF 
                
            f.close() 
            returnedhash =  "%016x" % hash 
            return returnedhash
        
        except(IOError): 
            return "IOError"