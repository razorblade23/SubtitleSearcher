from SubtitleSearcher.main import sg

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
                            [sg.InputText(disabled=True, key='SINGLEFILE', 
                                            default_text='Browse this to select a single file !', 
                                            disabled_readonly_text_color='red'), 
                                sg.FileBrowse('Browse', size=(8,2), initial_folder='~/Downloads', key='ChooseSingle', 
                                                file_types=(('Video files', '.avi'),('Video files', '.mkv'),))], 
                            [sg.InputText(disabled=True, key='MULTIPLEFILES', default_text='Browse this to select multiple files !', 
                                            disabled_readonly_text_color='red'), 
                            sg.FilesBrowse('Browse', size=(8,2), key='ChooseMultiple', initial_folder='~/Downloads',
                                            file_types=(('Video files', '.avi'),('Video files', '.mkv'),))],
                            [sg.Button('Search for single file', key='SEARCHBYSINGLEFILE', disabled=True), sg.Button('Search multiple files', key='SEARCHBYMULTIFILE', disabled=True)]
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
                        [sg.Checkbox('Keep on top ?', key='KeepOnTop')]
                    ])],
                    [sg.Button('Save', key='Save')]
        ])]
            ])],
            [sg.Tab(title='Languages', layout=[
                [sg.Text('Choose a language for search', font='Any 14')],
                [sg.Radio('Croatian', key='LangCRO', default=True, group_id=1), sg.Radio('English', key='LangENG', group_id=1), sg.Radio('Serbian', key='LangSRB', group_id=1), sg.Radio('Bosnian', key='LangBOS', group_id=1), sg.Radio('Slovenian', key='LangSLO', group_id=1)]
            ])],
            [sg.Tab(title='openSubtitles', layout=[
                [sg.Text('You must input your opensubtitles account information !')],
                [sg.InputText('Username', key='openUSERNAME')],
                [sg.InputText('Password', key='openPASS')]
            ])]
        ])]
    ]
    return layout

def subs_window():
    layout = [
        [sg.Frame(title='Selected movie metadata', layout=[
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
            sg.Column(layout=[
                [sg.T('Wrong movie / tv show?')],
                [sg.B('Change movie/tv show', key='CHANGEMOVIE')]
            ])],
        ]),
        sg.Frame(title='Options', layout=[
            [sg.Checkbox('Match subtitle filename with movie filename?', default=True)], [sg.Checkbox('Append language code to end of subtitle file?')]
        ])],
        [sg.Frame(title='Select subtitle', layout=[
            [sg.Listbox(values=[['1','2','3'],['4','4','4']], key='SUBSTABLE', size=(80,20), select_mode='LISTBOX_SELECT_MODE_SINGLE', enable_events=True)]
        ]),
        sg.Frame(title='Selected file metadata', layout=[
            [sg.Column(layout=[
                [sg.T('Subtitle name:')],
                [sg.T(key='SUBNAME', text_color='white', size=(65,1))]
            ])],
            [sg.Column(layout=[
                [sg.T('Subtitle extension:')],
                [sg.T(key='SUBEXTENSION', text_color='white', size=(10,1))]
            ])],
            [sg.Column(layout=[
                [sg.T('Subtitle language:')],
                [sg.T(key='SUBLANG', text_color='white', size=(10,1))]
            ])],
            [sg.Column(layout=[
                [sg.T('Subtitle downloads count:')],
                [sg.T(key='SUBDOWNCOUNT', text_color='white', size=(10,1))]
            ])],
            [sg.Column(layout=[
                [sg.T('Subtitle score:')],
                [sg.T(key='SUBSCORE', text_color='white', size=(10,1))]
            ])],
        ])],
        [sg.Button('Download', key='DOWNLOADSUB', disabled=True)],
        [sg.StatusBar('', key='STATUSBAR', size=(60,1))]
    ]
    return layout