# Import modules
from SubtitleSearcher.main import sg

'''
This script contains all GUI windows, their elements and starting settings

This is well documented in PySimpleGUI module, so nothing special to add about it

Separating windows like this allows you to re-build them when ever you want, as you cannot re-use already build window.

For all of documentation please see PySimpleGui documentation
https://pysimplegui.readthedocs.io/en/latest/

'''

sg.theme('DarkBrown4')

main_menu = [['File', ['Select a file', 'MultyFileWindow']],
            ['Log in to services', ['OpenSubtitles', 'Titlovi.com']],
            ['More info', ['!Set API key', 'About']]]

def openSubtitlesWindow():
    layout = [
        [sg.Text('''
        Search and download subtitles for movies and TV-Series from OpenSubtitles.org. 
        Search in 75 languages, 4.000.000+ subtitles, daily updates.''', font='Any 14', pad=(200,0))],
        [sg.Column(layout=[
            [sg.Image(source='images/OpenSubtitles_logo.png')]
        ]),
        sg.pin(sg.Column(pad=(100,0), visible=False, key='USERLOGGEDIN', layout=[
            [sg.Text('User ID')],
            [sg.Text(key='OpenSubtitlesUserID', font='Any 12', text_color='green')],
            [sg.Text('User level')],
            [sg.Text(key='OpenSubtitlesUserLevel', font='Any 12', text_color='green')],
            [sg.Text('Allowed download per 24 hours')],
            [sg.Text(key='OpenSubtitlesUserAllDownloads', font='Any 12', text_color='green')],
            [sg.Text('VIP status?')],
            [sg.Text(key='OpenSubtitlesUserVIP', font='Any 12', text_color='green')],
            [sg.Button('Log out', key='OpenSubtitlesLOGOUT')]
        ])),
        sg.Column(pad=((100,0),(0,0)), key='LOGINUSER', layout=[
            [sg.Text('Username:')],
            [sg.Input(key='OpenSubtitlesUSERNAME', size=(16,0), focus=True)],
            [sg.Text('Password:')],
            [sg.Input(key='OpenSubtitlesPASSWORD', password_char='*', size=(16,0))],
            [sg.Checkbox('Remember me?', tooltip='Plain JSON save, no security', key='RememberMe')],
            [sg.Button('Log in', key='OpenSubtitlesSUBMIT', enable_events=True)]
        ])]
    ]
    return layout

def TitloviLoginWindow():
    layout = [
        [sg.Text('Najve??a baza titlova za filmove, TV serije i dokumentarce.', font='Any 14', justification='center')],
        [sg.Text('''
                You must log in to Titlovi.com to use their engine for search and download.
                        You will get a token that lasts for 7 days (1 week).
                After that you need to re-activate by entering your username and password again.    
                ''', justification='center', font='Any 12')],
        [sg.Column(pad=((0,20), (0,0)), layout=[
            [sg.Image(source='images/titlovi_logo.png')]
        ]),
        sg.pin(sg.Column(key='USERLOGGEDIN', visible=False, layout=[
            [sg.Text('User ID', text_color='green')],
            [sg.Text(key='TitloviUSERID', text_color='white')],
            [sg.Text('User token', text_color='green')],
            [sg.Text(key='TitloviTOKEN', text_color='white')],
            [sg.Text('Token is active for this number of days', text_color='green')],
            [sg.Text(key='TitloviEXPIRY', text_color='white')]
        ])),
        sg.Column(pad=((100,0),(0,0)), key='LOGINUSER', layout=[
            [sg.Text('Username:')],
            [sg.Input(key='TitloviUSERNAME', size=(16,0), focus=True)],
            [sg.Text('Password:')],
            [sg.Input(key='TitloviPASSWORD', password_char='*', size=(16,0))],
            [sg.Checkbox('Remember me?', enable_events=True, tooltip='Plain JSON save, no security', key='RememberMe')],
            [sg.Button('Log in', key='LOGIN', enable_events=True)]
        ])]
    ]
    return layout

def AboutWindow():
    layout = [
        [sg.Image(source='images/logo.png')],
        [sg.Text('We were just two guys with an idea.', font='Any 13')],
        [sg.Text('Well one had idea, other had a year\nof programming experience in Python', font='Any 13')],
        [sg.Text('We are now proudly in beta testing stage', font='Any 16', text_color='white')],
        [sg.Text('We are licenced under MIT licence', font='Any 12', text_color='white')],
        [sg.Text('')],
        [sg.Text('We want to thank to our sources.', font='Any 14')],
        [sg.Text('For now there are 2 sources to work with', font='Any 12')],
        [sg.Text('We are powered by (for now):', font='Any 14', text_color='green')],
        [sg.Column(pad=(20,50), layout=[
            [sg.Image(source='images/OpenSubtitles_logo.png')]
        ]),
        sg.Column(pad=(20,50), layout=[
            [sg.Image(source='images/titlovi_logo.png')]
        ])]
    ]
    return layout

def main_window():
    layout = [
        [sg.Menu(main_menu)],
        [sg.Image(source='images/logo.png')],
        [sg.Text('Project aiming to make finding and downloading subtitles a breeze!', font='Any 16')],
        [sg.TabGroup(enable_events=True, key='MainTabGroup', layout=[
            [sg.Tab(title='Main', key='MainTab', layout=[
                [sg.Frame(title='Search for subtitles', layout=[
                    [sg.TabGroup(layout=[
                        [sg.Tab(title='Search by file', layout=[
                            [sg.Button(image_filename='images/filefind.png',tooltip='Browse', key='BROWSE', pad=(50,0)),
                            sg.Button(image_filename='images/Search44.png', tooltip='Search for subtitles', key='SEARCHFORSUBS', pad=(50,0))],
                        ])],
                        [sg.Tab(title='Search by IMDB ID', disabled=True, layout=[
                            [sg.Frame(title='ID', layout=[
                                [sg.Text('Enter IMDB ID')],
                                [sg.InputText(key='IMDBID', size=(8,1))],
                                [sg.Button('Search for movie subtitles', key='SEARCHBYIMDB', disabled=False), sg.Button('Search for movie on IMDB', key='SEARCHONIMDB')]
                            ]), sg.Frame(title='Rezultat', layout=[
                                [sg.Text('', key='MovieTitle')],
                                [sg.Text('', key='MovieYear')]
                            ])]
                        ])]
                    ])]
            ]),
                sg.Frame(title='Select options', layout=[
                    [sg.Checkbox('Use opensubtitles.org ?', key='USEOPEN', default=True)],
                    [sg.Checkbox('Use titlovi.com ?', key='USETITLOVI', disabled=True)],
                    [sg.Checkbox('Use podnapisi.net ?', disabled=True)],
                    [sg.Checkbox('Use openSubtitles ?', disabled=True)],
                    [sg.Frame(title='Additional settings', layout=[
                        [sg.Checkbox('Remember last folder', key='RememberLastFolder', default=True)],
                        [sg.Checkbox('Quick mode ?', key='QuickMode')],
                        [sg.Checkbox('Keep on top ?', key='KeepOnTop')]
                    ])],
                    [sg.Button('Save', key='Save')]
        ])]
            ])],
            [sg.Tab(title='Languages', key='LangTab', layout=[
                [sg.Text('Choose a language for search', font='Any 14')],
                [sg.Checkbox('Croatian', key='LangCRO', default=True), 
                sg.Checkbox('English', key='LangENG'), 
                sg.Checkbox('Serbian', key='LangSRB'), 
                sg.Checkbox('Bosnian', key='LangBOS'), 
                sg.Checkbox('Slovenian', key='LangSLO')]
            ])]
        ])],
        [sg.ProgressBar(100, 'h', key='PROGRESSBAR', bar_color=('green', 'black')), sg.Text('Working, please wait', key='WORKINGSTRING', visible=False)],
        [sg.StatusBar('SubbyDoo - alpha', key='STATUSBAR1', size=(30,1), justification='center'), 
        sg.StatusBar('OpenSubtitles.org', key='STATUSBAR2', size=(30,1), justification='center'),
        sg.StatusBar('Titlovi.com', key='STATUSBAR3', size=(30,1), justification='center'),
        sg.StatusBar('', key='STATUSBAR4', size=(30,1), justification='right'),]
    ]
    return layout

def subs_window():
    layout = [
        [sg.Frame(title='Selected file metadata', layout=[
            [sg.Column(layout=[
                [sg.T('Name:')],
                [sg.T(key='MOVIENAME', text_color='white', size=(26,1))]
            ]),
            sg.Column(layout=[
                [sg.T('Year:')],
                [sg.T(key='MOVIEYEAR', text_color='white', size=(5,1))]
            ]),
            sg.Column(layout=[
                [sg.T('IMDB ID:')],
                [sg.T(key='IMDBID', text_color='white', size=(8,1))]
            ]),
            sg.Column(layout=[
                [sg.T('Kind:')],
                [sg.T(key='KIND', text_color='white', size=(12,1))]
            ]),
            sg.Column(key='TVSERIESINFO', visible=False, layout=[
                [sg.T('Season:'),
                sg.T(key='SEASON', text_color='white', size=(15,1))],
                [sg.T('Episode:'),
                sg.T(key='EPISODE', text_color='white', size=(15,1))]
            ]),
            sg.Column(layout=[
                [sg.T('Wrong movie/tv show?')],
                [sg.B('Change movie/tv show', key='CHANGEMOVIE')]
            ])],
        [sg.Text('Filename:')],
        [sg.T(key='VIDEOFILENAME', text_color='white')]]),
        sg.Frame(title='Options', layout=[
            [sg.Checkbox('Match subtitle filename with movie filename?', default=True)], [sg.Checkbox('Append language code to end of subtitle file?', default=True, key='AppendLangCode')]
        ])],
        [sg.Frame(title='Select subtitle', layout=[
            [sg.Listbox(values=[' '],
                        size=(120,20),
                        key='SUBSTABLE',
                        select_mode='browse', 
                        enable_events=True)]
        ]),
        sg.Frame(title='Selected subtitle metadata', layout=[
            [sg.Column(layout=[
                [sg.T('Found using: '), sg.T(key='ENGINE', text_color='#00acb5', font='Any 14')],
                [sg.T('Subtitle name:', size=(20,1)), sg.T('TRUSTED UPLOADER', text_color='green', visible=False, key='TRUSTED')],
                [sg.T(key='SUBNAME', text_color='white')]
            ])],
            [sg.Column(layout=[
                [sg.T('Subtitle user ID: '),
                sg.T(key='SUBUSERID', text_color='white')],
                [sg.T('Subtitle user nickname: '),
                sg.T(key='SUBUSERNICK', text_color='white')],
                [sg.T('Subtitle author comment: ')],
                [sg.Multiline('No comment', key='SUBUSERCOMMENT', text_color='white', size=(60,3), no_scrollbar=True)],
                [sg.T('Subtitle add date: '),
                sg.T(key='SUBADDDATE', text_color='white')],
            ])],
            [sg.Column(layout=[
                [sg.T('Subtitle extension: '),
                sg.T(key='SUBEXTENSION', text_color='white')],
                [sg.T('Subtitle language: '),
                sg.T(key='SUBLANG', text_color='white')]
            ])],
            [sg.Column(layout=[
                [sg.T('Subtitle downloads count: '),
                sg.T(key='SUBDOWNCOUNT', text_color='white')]
            ])],
            [sg.Column(layout=[
                [sg.T('Subtitle score: '),
                sg.T(key='SUBSCORE', text_color='white')]
            ])],
        ])],
        [sg.Button('Download', key='DOWNLOADSUB', disabled=True)],
        [sg.StatusBar('', key='STATUSBAR', size=(60,1))]
    ]
    return layout

def multyfileSelectWindow():
    layout = [
        [sg.Text('Video title:')],
        [sg.Text(key='VideoTitle')],
        [sg.Frame(title='Files selected', layout=[
            [sg.Listbox(values=['File1', 'File2', 'File3'], size=(45,10), key='ListBox1')],
        ]),
        sg.Frame(title='Subtitles found for selected file', layout=[
            [sg.Listbox(values=['Subtitle 1', 'Subtitle 2', 'Subtitle 3'], size=(60,10), key='ListBox2'),
            sg.Button(image_filename='images/edit_add.png', image_subsample=4, tooltip='Add to download list')]
        ]),
        sg.Frame(title='Selected subtitles for download', layout=[
            [sg.Listbox(values=['SUB ID 1', 'SUB ID 2', 'SUB ID 3'], size=(15,10), key='ListBox2'),
            sg.Column(layout=[
                [sg.Button(image_filename='images/button_cancel.png', image_subsample=4, tooltip='Clear download list')], 
                [sg.Button(image_filename='images/Creative player 256_green.png', image_subsample=8, tooltip='Download subtitles')]
            ])]
        ])]
    ]
    return layout