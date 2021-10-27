from SubtitleSearcher.imdb_metadata import search_by_id

class Movie:
    def __init__(self, byte_size, file_hash):
        self.byte_size = byte_size
        self.file_hash = file_hash

    def set_metadata(self, name, year, download_link, zip_download_link, imdb_id):
        self.name = name
        self.year = year
        self.download_link = download_link
        self.zip_download_link = zip_download_link
        self.imdb_id = imdb_id
    
    def add_imdb_metadata(self):
        imdb_response = search_by_id(self.imdb_id)

class MovieSubtitle(Movie):
    pass