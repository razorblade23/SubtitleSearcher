from os import access
import PTN
from contextlib import suppress
from SubtitleSearcher.data import starting_settings
import json
from collections import namedtuple

class Movie:
    def __init__(self, byte_size, file_hash, file_path, file_name):
        self.byte_size = byte_size
        self.file_hash = file_hash
        self.file_path = file_path
        self.file_name = file_name

        self.audio = None
        self.bitDepth = None
        self.codec = None
        self.day = None
        self.directorsCut = None
        self.documentary = None
        self.encoder = None
        self.episode = None
        self.episodeName = None
        self.excess = None
        self.extended = None
        self.filetype = None
        self.fps = None
        self.genre = None
        self.hardcoded = None
        self.hdr = None
        self.internal = None
        self.internationalCut = None
        self.language = None
        self.limited = None
        self.month = None
        self.network = None
        self.proper = None
        self.quality = None
        self.readnfo = None
        self.region = None
        self.remastered = None
        self.remux = None
        self.repack = None
        self.resolution = None
        self.sbs = None
        self.season = None
        self.site = None
        self.size = None
        self.subtitles = None
        self.title = None
        self.unrated = None
        self.untouched = None
        self.upscaled = None
        self.widescreen = None
        self.year = None
        self.threeD = None

    def set_from_filename(self):
        self.movie_info = PTN.parse(self.file_name, standardise=False)
        with suppress(KeyError): self.audio = self.movie_info['audio']
        with suppress(KeyError): self.bitDepth = self.movie_info['bitDepth']
        with suppress(KeyError): self.codec = self.movie_info['codec']
        with suppress(KeyError): self.day = self.movie_info['day']
        with suppress(KeyError): self.directorsCut = self.movie_info['directorsCut']
        with suppress(KeyError): self.documentary = self.movie_info['documentary']
        with suppress(KeyError): self.encoder = self.movie_info['encoder']
        with suppress(KeyError): self.episode = self.movie_info['episode']
        with suppress(KeyError): self.episodeName = self.movie_info['episodeName']
        with suppress(KeyError): self.excess = self.movie_info['excess']
        with suppress(KeyError): self.extended = self.movie_info['extended']
        with suppress(KeyError): self.filetype = self.movie_info['filetype']
        with suppress(KeyError): self.fps = self.movie_info['fps']
        with suppress(KeyError): self.genre = self.movie_info['genre']
        with suppress(KeyError): self.hardcoded = self.movie_info['hardcoded']
        with suppress(KeyError): self.hdr = self.movie_info['hdr']
        with suppress(KeyError): self.internal = self.movie_info['internal']
        with suppress(KeyError): self.internationalCut = self.movie_info['internationalCut']
        with suppress(KeyError): self.language = self.movie_info['language']
        with suppress(KeyError): self.limited = self.movie_info['limited']
        with suppress(KeyError): self.month = self.movie_info['month']
        with suppress(KeyError): self.network = self.movie_info['network']
        with suppress(KeyError): self.proper = self.movie_info['proper']
        with suppress(KeyError): self.quality = self.movie_info['quality']
        with suppress(KeyError): self.readnfo = self.movie_info['readnfo']
        with suppress(KeyError): self.region = self.movie_info['region']
        with suppress(KeyError): self.remastered = self.movie_info['remastered']
        with suppress(KeyError): self.remux = self.movie_info['remux']
        with suppress(KeyError): self.repack = self.movie_info['repack']
        with suppress(KeyError): self.resolution = self.movie_info['resolution']
        with suppress(KeyError): self.sbs = self.movie_info['sbs']
        with suppress(KeyError): self.season = self.movie_info['season']
        with suppress(KeyError): self.site = self.movie_info['site']
        with suppress(KeyError): self.size = self.movie_info['size']
        with suppress(KeyError): self.subtitles = self.movie_info['subtitles']
        with suppress(KeyError): self.title = self.movie_info['title']
        with suppress(KeyError): self.unrated = self.movie_info['unrated']
        with suppress(KeyError): self.untouched = self.movie_info['untouched']
        with suppress(KeyError): self.upscaled = self.movie_info['upscaled']
        with suppress(KeyError): self.widescreen = self.movie_info['widescreen']
        with suppress(KeyError): self.year = self.movie_info['year']
        with suppress(KeyError): self.threeD = self.movie_info['3d']

        
    # Function to convert  
    def listToString(self, s): 
        
        # initialize an empty string
        str1 = " " 
        
        # return string  
        return (str1.join(s))

    def set_imdb_id(self, imdb_id):
        self.imdb_id = imdb_id
    
    def set_movie_kind(self, kind):
        self.kind = kind

def load_from_json(subtitle):
    return namedtuple('X', subtitle.keys())(*subtitle.values())
    
class titloviComSub:
    def __init__(self, subtitle):
        self.engine = 'Titlovi'
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