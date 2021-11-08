from SubtitleSearcher.data import handle_zip
import threading
import time

def ZipDownloaderThreaded(file_name, zip_down_link, values):
    zip_handler = handle_zip.ZipHandler(file_name, zip_down_link, values['SINGLEFILE'])
    file_download = zip_handler.download_zip()
    if file_download:
        zip_handler.extract_zip()
        zip_handler.move_files()
        zip_handler.delete_remains()


THREAD1 = threading.Thread(target=ZipDownloaderThreaded, args=[])
