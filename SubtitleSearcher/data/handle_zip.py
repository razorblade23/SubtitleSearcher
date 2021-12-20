# Importing modules
import zipfile
import requests
import os
from zipfile import ZipFile
import shutil

# Move subtitles (OpenSubtitles.com)
def move_subtitle(mode, source_path, dst_path, append_lang_code=None):
    org_string = dst_path
    size = len(org_string)
    mod_string = org_string[:size - 4]
    if append_lang_code != None:
        mod_string = f'{mod_string}-{append_lang_code}'
    if mode == 'zip':
        final_path = os.path.join(dst_path, f'{mod_string}.zip')
    if mode == 'srt':
        final_path = os.path.join(dst_path, f'{mod_string}.srt')
    shutil.move(source_path, final_path)

# Move subtitles (Titlovi.com)
class SubFileHandler:
    '''
    Base class of File Handler. Not to be called directly. Instantiate from child classes.
    Used to handle all common operations with subtitle files like downloading and unzipping.

    Child classes handle diffrent aproaches by diffrent sources
    '''
    def __init__(self):
        self.download_folder = 'downloaded'
        self.extracted_folder = 'extracted'
        self.zip_name = 'sub.zip'
        self.extracted_zip = os.path.join(self.extracted_folder, self.zip_name)
    
    @staticmethod
    def check_for_folders():
        if not os.path.isdir('downloaded'):
            os.makedirs('downloaded')
        if not os.path.isdir('extracted'):
            os.makedirs('extracted')
    
    def download_zip(self, url):
        self.check_for_folders()
        success = False
        try:
            r = requests.get(url, allow_redirects=True, timeout=20)
            open('downloaded/sub.zip', 'wb').write(r.content)
        except:
            success = False
        else:
            success = True
        return success

    def list_all_extracted(self):
        extracted_files = os.listdir(self.extracted_folder)
        return extracted_files

    def get_zip(self):
        if os.path.isdir('downloaded'):
            try:
                path = os.path.join(self.download_folder, self.zip_name)
            except:
                pass
            else:
                return path
    
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
    def __init__(self):
        super().__init__()
    
    def download_zip(self, url):
        return super().download_zip(url)

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
    
    def move_files(self, dst_path, filename, append_lang_code=None):
        src_path = os.path.join(self.extracted_folder, filename)
        org_string = dst_path
        size = len(org_string)
        mod_string = org_string[:size - 4]
        if append_lang_code != None:
            mod_string = f'{mod_string}-{append_lang_code}'
        final_path = os.path.join(dst_path, f'{mod_string}.srt')
        shutil.move(src_path, final_path)

class TitloviFileHandler(SubFileHandler):
    def __init__(self):
        super().__init__()
    
    def download(self, url):
        self.download_zip(url)
    
    def move_file(self, dst_folder, append_lang_code=None):
        src_path = os.path.join(self.download_folder, self.zip_name)
        org_string = dst_folder
        size = len(org_string)
        mod_string = org_string[:size - 4]
        if append_lang_code != None:
            mod_string = f'{mod_string}-{append_lang_code}'
        final_path = os.path.join(dst_folder, f'{mod_string}.zip')
        shutil.move(src_path, final_path)



