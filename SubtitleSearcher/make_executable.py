'''
    Run this script to build executable
'''

import PyInstaller.__main__

PyInstaller.__main__.run([
    'run.py',
    '-D',
    '--add-data=images:images',
    '--clean',
    '-n SubbyDoo',
    '-y',
])