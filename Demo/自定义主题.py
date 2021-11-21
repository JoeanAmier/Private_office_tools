import PySimpleGUI as sg

# Add your new theme colors and settings
my_new_theme = {'BACKGROUND': '#709053',
                'TEXT': '#fff4c9',
                'INPUT': '#c7e78b',
                'TEXT_INPUT': '#000000',
                'SCROLL': '#c7e78b',
                'BUTTON': ('white', '#709053'),
                'PROGRESS': ('#01826B', '#D0D0D0'),
                'BORDER': 1,
                'SLIDER_DEPTH': 0,
                'PROGRESS_DEPTH': 0}

# Add your dictionary to the PySimpleGUI themes
sg.theme_add_new('MyNewTheme', my_new_theme)

# Switch your theme to use the newly added one. You can add spaces to make
# it more readable
sg.theme('My New Theme')

# Call a popup to show what the theme looks like
sg.popup_get_text('This how the MyNewTheme custom theme looks')
