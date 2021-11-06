import PTN
from contextlib import suppress

class Movie:
    def __init__(self, byte_size, file_hash, file_path, file_name):
        self.byte_size = byte_size
        self.file_hash = file_hash
        self.file_path = file_path
        self.file_name = file_name

        self.audio = ''
        self.codec = ''
        self.container = ''
        self.episode = ''
        self.episodeName = ''
        self.excess = ''
        self.extended = ''
        self.garbage = ''
        self.group = ''
        self.hardcoded = ''
        self.language = ''
        self.proper = ''
        self.quality = ''
        self.region = ''
        self.repack = ''
        self.resolution = ''
        self.season = ''
        self.title = ''
        self.website = ''
        self.widescreen = ''
        self.year = ''

    def set_from_filename(self):
        self.movie_info = PTN.parse(self.file_name)
        with suppress(KeyError): self.audio = self.movie_info['audio']
        with suppress(KeyError): self.codec = self.movie_info['codec']
        with suppress(KeyError): self.container = self.movie_info['container']
        with suppress(KeyError): self.episode = self.movie_info['episode']
        with suppress(KeyError): self.episodeName = self.movie_info['episodeName']
        with suppress(KeyError): self.excess = self.movie_info['excess']
        with suppress(KeyError): self.extended = self.movie_info['extended']
        with suppress(KeyError): self.garbage = self.movie_info['garbage']
        with suppress(KeyError): self.group = self.movie_info['group']
        with suppress(KeyError): self.hardcoded = self.movie_info['hardcoded']
        with suppress(KeyError): self.language = self.movie_info['language']
        with suppress(KeyError): self.proper = self.movie_info['proper']
        with suppress(KeyError): self.quality = self.movie_info['quality']
        with suppress(KeyError): self.region = self.movie_info['region']
        with suppress(KeyError): self.repack = self.movie_info['repack']
        with suppress(KeyError): self.resolution = self.movie_info['resolution']
        with suppress(KeyError): self.season = self.movie_info['season']
        with suppress(KeyError): self.title = self.movie_info['title']
        with suppress(KeyError): self.website = self.movie_info['website']
        with suppress(KeyError): self.widescreen = self.movie_info['widescreen']
        with suppress(KeyError): self.year = self.movie_info['year']
        

    def set_imdb_id(self, imdb_id):
        self.imdb_id = imdb_id
    
    def set_movie_kind(self, kind):
        self.kind = kind

class Subtitle():
    def __init__(self, sub_file_name, sub_lang_id, sub_format, sub_download_count, sub_download_link, sub_zip_donwload_link, score):
        self.sub_file_name = sub_file_name
        self.sub_lang_id = sub_lang_id
        self.sub_format = sub_format
        self.sub_download_count = sub_download_count
        self.sub_download_link = sub_download_link
        self.sub_zip_donwload_link = sub_zip_donwload_link
        self.score = score