from SubtitleSearcher.main import sg
from psgtray import SystemTray

sg.theme('DarkBrown4')

def main_window():
    layout = [
        [sg.Image(source='SubtitleSearcher/static/images/logo.png')],
        [sg.Text('Project aiming to make finding and downloading subtitles a breeze!', font='Any 16')],
        [sg.TabGroup(layout=[
            [sg.Tab(title='Main', layout=[
                [sg.Frame(title='Search for subtitles', layout=[
                    [sg.TabGroup(layout=[
                        [sg.Tab(title='Search by file', layout=[
                            [sg.Button('Browse', key='BROWSE', size=(5,2), font='Any 30'),
                            sg.Button('Search for subtitles', key='SEARCHFORSUBS', size=(15,2), font='Any 30')],
                            [sg.Column(key='FILEINFOFRONT', layout=[
                                [sg.Frame(title='File information', layout=[
                                    [sg.Column(layout=[
                                        [sg.T('Video name:')],
                                        [sg.T('', key='VIDEONAMEFRONT', size=(20,1))]
                                    ]),
                                    sg.Column(layout=[
                                        [sg.T('Video year:')],
                                        [sg.T('', key='VIDEOYEARFRONT', size=(6,1))]
                                    ]),
                                    sg.Column(layout=[
                                        [sg.T('Video kind:')],
                                        [sg.T('', key='VIDEOKINDFRONT', size=(14,1))]
                                    ]),
                                    sg.Column(layout=[
                                        [sg.T('Video resoulution:')],
                                        [sg.T('', key='VIDEORESFRONT', size=(10,1))]
                                    ])],
                                ])]
                            ])]
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
                    [sg.Checkbox('Use titlovi.com ?', disabled=True)],
                    [sg.Checkbox('Use podnapisi.net ?', disabled=True)],
                    [sg.Checkbox('Use openSubtitles ?', disabled=True)],
                    [sg.Frame(title='Additional settings', layout=[
                        [sg.Checkbox('Quick mode ?', key='QuickMode')],
                        [sg.Checkbox('Keep on top ?', key='KeepOnTop')]
                    ])],
                    [sg.Button('Save', key='Save')]
        ])]
            ])],
            [sg.Tab(title='Languages', layout=[
                [sg.Text('Choose a language for search', font='Any 14')],
                [sg.Radio('Croatian', key='LangCRO', default=True, group_id=1), 
                sg.Radio('English', key='LangENG', group_id=1), 
                sg.Radio('Serbian', key='LangSRB', group_id=1), 
                sg.Radio('Bosnian', key='LangBOS', group_id=1), 
                sg.Radio('Slovenian', key='LangSLO', group_id=1)]
            ])],
            [sg.Tab(title='openSubtitles', layout=[
                [sg.Text('You must input your opensubtitles account information !')],
                [sg.InputText('Username', key='openUSERNAME')],
                [sg.InputText('Password', key='openPASS')]
            ])]
        ])],
        [sg.ProgressBar(100, 'h', key='PROGRESSBAR', bar_color=('green', 'black')), sg.Text('Working, please wait', key='WORKINGSTRING', visible=False)],
        [sg.StatusBar('', key='STATUSBAR', size=(90,1)), sg.StatusBar('', key='STATUSBAR1', size=(10,1), justification='right')]
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
            [sg.Checkbox('Match subtitle filename with movie filename?', default=True)], [sg.Checkbox('Append language code to end of subtitle file?')]
        ])],
        [sg.Frame(title='Select subtitle', layout=[
            [sg.Listbox(values=[''], key='SUBSTABLE', size=(80,20), select_mode='LISTBOX_SELECT_MODE_SINGLE', enable_events=True)]
        ]),
        sg.Frame(title='Selected subtitle metadata', layout=[
            [sg.Column(layout=[
                [sg.T('Subtitle name:')],
                [sg.T(key='SUBNAME', text_color='white', size=(65,1))]
            ])],
            [sg.Column(layout=[
                [sg.T('Subtitle user ID: '),
                sg.T(key='SUBUSERID', text_color='white', size=(10,1))],
                [sg.T('Subtitle user nickname: '),
                sg.T(key='SUBUSERNICK', text_color='white', size=(16,1))],
                [sg.T('Subtitle author comment: '),
                sg.T(key='SUBUSERCOMMENT', text_color='white', size=(16,1))],
                [sg.T('Subtitle add date: '),
                sg.T(key='SUBADDDATE', text_color='white', size=(20,1))],
            ])],
            [sg.Column(layout=[
                [sg.T('Subtitle extension: '),
                sg.T(key='SUBEXTENSION', text_color='white', size=(10,1))],
                [sg.T('Subtitle language: '),
                sg.T(key='SUBLANG', text_color='white', size=(10,1))]
            ])],
            [sg.Column(layout=[
                [sg.T('Subtitle downloads count: '),
                sg.T(key='SUBDOWNCOUNT', text_color='white', size=(10,1))]
            ])],
            [sg.Column(layout=[
                [sg.T('Subtitle score: '),
                sg.T(key='SUBSCORE', text_color='white', size=(10,1))]
            ])],
        ])],
        [sg.Button('Download', key='DOWNLOADSUB', disabled=True)],
        [sg.StatusBar('', key='STATUSBAR', size=(60,1))]
    ]
    return layout