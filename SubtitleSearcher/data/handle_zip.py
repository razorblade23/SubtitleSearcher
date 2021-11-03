import requests
import os

def check_for_folders():
    if not os.path.isdir('downloaded'):
        os.makedirs('downloaded')
    if not os.path.isdir('extracted'):
        os.makedirs('extracted')

def download_zip(url):
    check_for_folders()
    r = requests.get(url, allow_redirects=True)
    open('downloaded/sub.zip', 'wb').write(r.content)
    print('File downloaded.\n File can be found in downloaded folder in zip format')