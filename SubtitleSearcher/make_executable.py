'''
    Run this script to build executable
'''

import PyInstaller.__main__

PyInstaller.__main__.run([
    'run.py',
    '--onedir',
    '--windowed',
    '--add-data=.:.'
])