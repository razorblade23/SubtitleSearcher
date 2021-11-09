from SubtitleSearcher.main import threading
import time

def ZipDownloaderThreaded(zip_handler, thread_nmb):
    file_download = zip_handler.download_zip()
    if file_download:
        print(f'Thread {thread_nmb} working with\n{zip_handler.filename}')
        print(f'Subtitle downloaded - thread {thread_nmb}')
        try:
            print(f'Extracting from ZIP - thread {thread_nmb}')
            zip_handler.extract_zip()
        except FileNotFoundError:
            print(f'Bad zip downloaded - thread {thread_nmb}')
        else:
            try:
                print(f'Moving files to target directory - thread {thread_nmb}')
                zip_handler.move_files()
            except FileNotFoundError:
                print(f'Cant move file - thread {thread_nmb}')
            else:
                print(f'Deleting remains from memory - thread {thread_nmb}')
                zip_handler.delete_remains()
                print(f'Job done, continuing - thread {thread_nmb}\n')
