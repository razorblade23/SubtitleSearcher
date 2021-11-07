from os import access
import PTN
from contextlib import suppress
from SubtitleSearcher.data import starting_settings

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
        if isinstance(self.excess, list):
            for excess in self.excess:
                if starting_settings.trusted_coders.count(excess):
                    self.excess = excess
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

class Subtitle():
    def __init__(self, subtitle):
        self.MatchedBy = subtitle['MatchedBy']
        self.IDSubtitleFile = subtitle['IDSubtitleFile']
        self.SubFileName = subtitle['SubFileName']
        self.SubActualCD = subtitle['SubActualCD']
        self.SubSize = subtitle['SubSize']
        self.SubHash = subtitle['SubHash']
        self.SubLastTS = subtitle['SubLastTS']
        self.SubTSGroup = subtitle['SubTSGroup']
        self.InfoReleaseGroup = subtitle['InfoReleaseGroup']
        self.InfoFormat = subtitle['InfoFormat']
        self.IDSubtitle = subtitle['IDSubtitle']
        self.UserID = subtitle['UserID']
        self.SubLanguageID = subtitle['SubLanguageID']
        self.SubFormat = subtitle['SubFormat']
        self.SubSumCD = subtitle['SubSumCD']
        self.SubAuthorComment = subtitle['SubAuthorComment']
        self.SubAddDate = subtitle['SubAddDate']
        self.SubBad = subtitle['SubBad']
        self.SubRating = subtitle['SubRating']
        self.SubSumVotes = subtitle['SubSumVotes']
        self.SubDownloadsCnt = subtitle['SubDownloadsCnt']
        self.MovieReleaseName = subtitle['MovieReleaseName']
        self.MovieFPS = subtitle['MovieFPS']
        self.IDMovie = subtitle['IDMovie']
        self.IDMovieImdb = subtitle['IDMovieImdb']
        self.MovieName = subtitle['MovieName']
        self.MovieNameEng = subtitle['MovieNameEng']
        self.MovieYear = subtitle['MovieYear']
        self.MovieImdbRating = subtitle['MovieImdbRating']
        self.UserNickName = subtitle['UserNickName']
        self.SubTranslator = subtitle['SubTranslator']
        self.ISO639 = subtitle['ISO639']
        self.LanguageName = subtitle['LanguageName']
        self.SubHearingImpaired = subtitle['SubHearingImpaired']
        self.UserRank = subtitle['UserRank']
        self.SeriesSeason = subtitle['SeriesSeason']
        self.SeriesEpisode = subtitle['SeriesEpisode']
        self.MovieKind = subtitle['MovieKind']
        self.SubDownloadLink = subtitle['SubDownloadLink']
        self.ZipDownloadLink = subtitle['ZipDownloadLink']
        self.SubtitlesLink = subtitle['SubtitlesLink']
        self.Score = subtitle['Score']