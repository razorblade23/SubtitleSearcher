import requests
import os
from zipfile import ZipFile
import shutil

def check_for_folders():
    if not os.path.isdir('downloaded'):
        os.makedirs('downloaded')
    if not os.path.isdir('extracted'):
        os.makedirs('extracted')

def download_zip(url):
    check_for_folders()
    success = False
    try:
        r = requests.get(url, allow_redirects=True)
        open('downloaded/sub.zip', 'wb').write(r.content)
    except:
        success = False
    else:
        success = True
    return success

def get_zip():
    if os.path.isdir('downloaded'):
        try:
            path = 'downloaded/sub.zip'
        except:
            pass
        else:
            return path

def extract_zip():
    # specifying the zip file name
    file_name = get_zip()
    
    # opening the zip file in READ mode
    with ZipFile(file_name, 'r') as zip:
        zip.extractall(path='extracted')

def move_files(filename, path_to_movie):
    src_path = f'extracted/{filename}'
    dst_path = f'{path_to_movie}.srt'
    shutil.move(src_path, dst_path)
