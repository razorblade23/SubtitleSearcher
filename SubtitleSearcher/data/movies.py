import PTN
from contextlib import suppress

class Movie:
    def __init__(self, byte_size, file_hash, file_path, file_name):
        self.byte_size = byte_size
        self.file_hash = file_hash
        self.file_path = file_path
        self.file_name = file_name

    def set_from_filename(self):
        movie_info = PTN.parse(self.file_name)
        with suppress(KeyError): self.audio = movie_info['audio']
        with suppress(KeyError): self.codec = movie_info['codec']
        with suppress(KeyError): self.container = movie_info['container']
        with suppress(KeyError): self.episode = movie_info['episode']
        with suppress(KeyError): self.episodeName = movie_info['episodeName']
        with suppress(KeyError): self.excess = movie_info['excess']
        with suppress(KeyError): self.extended = movie_info['extended']
        with suppress(KeyError): self.garbage = movie_info['garbage']
        with suppress(KeyError): self.group = movie_info['group']
        with suppress(KeyError): self.hardcoded = movie_info['hardcoded']
        with suppress(KeyError): self.language = movie_info['language']
        with suppress(KeyError): self.proper = movie_info['proper']
        with suppress(KeyError): self.quality = movie_info['quality']
        with suppress(KeyError): self.region = movie_info['region']
        with suppress(KeyError): self.repack = movie_info['repack']
        with suppress(KeyError): self.resolution = movie_info['resolution']
        with suppress(KeyError): self.season = movie_info['season']
        with suppress(KeyError): self.title = movie_info['title']
        with suppress(KeyError): self.website = movie_info['website']
        with suppress(KeyError): self.widescreen = movie_info['widescreen']
        with suppress(KeyError): self.year = movie_info['year']

    def set_imdb_id(self, imdb_id):
        self.imdb_id = imdb_id
    
    def set_movie_kind(self, kind):
        self.kind = kind

class MovieSubtitle():
    def __init__(self, sub_file_name, sub_lang_id, sub_format, sub_download_count, sub_download_link, sub_zip_donwload_link, score):
        self.sub_file_name = sub_file_name
        self.sub_lang_id = sub_lang_id
        self.sub_format = sub_format
        self.sub_download_count = sub_download_count
        self.sub_download_link = sub_download_link
        self.sub_zip_donwload_link = sub_zip_donwload_link
        self.score = score