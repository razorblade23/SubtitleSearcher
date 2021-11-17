import zipfile
import requests
import os
from zipfile import ZipFile
import shutil


class SubFileHandler:
    '''
    Base class of File Handler. Not to be called directly. Instantiate from child classes.
    Used to handle all common operations with subtitle files like downloading and unzipping.

    Child classes handle diffrent aproaches by diffrent sources
    '''
    def __init__(self, url_for_download, movie_folder=None, filename=None):
        self.download_folder = 'downloaded'
        self.extracted_folder = 'extracted'
        self.zip_name = 'sub.zip'
        self.downloaded_zip = os.path.join(self.extracted_folder, self.zip_name)
        self.filename = filename
        self.url = url_for_download
        self.movie_folder = movie_folder
    
    def check_for_folders(self):
        if not os.path.isdir('downloaded'):
            os.makedirs('downloaded')
        if not os.path.isdir('extracted'):
            os.makedirs('extracted')
    
    def download_zip(self):
        self.check_for_folders()
        success = False
        try:
            r = requests.get(self.url, allow_redirects=True)
            open('downloaded/sub.zip', 'wb').write(r.content)
        except:
            success = False
        else:
            success = True
        return success

    def get_zip(self):
        if os.path.isdir('downloaded'):
            try:
                path = 'downloaded/sub.zip'
            except:
                pass
            else:
                return path

    def extract_zip(self):
        # specifying the zip file name
        file_name = self.get_zip()
        # opening the zip file in READ mode
        try:
            with ZipFile(file_name, 'r') as zip:
                zip.extractall(path='extracted')
        except zipfile.BadZipFile:
            print('Bad zip, cant continue')
            return
    
    def move_files(self, append_lang_code=None):
        src_path = f'extracted/{self.filename}'
        org_string = self.movie_folder
        size = len(org_string)
        mod_string = org_string[:size - 4]
        if append_lang_code != None:
            mod_string = f'{mod_string}-{append_lang_code}'
        dst_path = f'{mod_string}.srt'
        shutil.move(src_path, dst_path)
    
    def delete_remains(self):
        with os.scandir(self.download_folder) as entries:
            for entry in entries:
                if entry.is_dir() and not entry.is_symlink():
                    shutil.rmtree(entry.path)
                else:
                    os.remove(entry.path)
        
        with os.scandir(self.extracted_folder) as entries:
            for entry in entries:
                if entry.is_dir() and not entry.is_symlink():
                    shutil.rmtree(entry.path)
                else:
                    os.remove(entry.path)

class OpenSubtitlesHandler(SubFileHandler):
    pass


class ZipHandlerTitlovi(SubFileHandler):
    def download_subtitle(self):
        self.download_zip()
        self.extract_zip()



