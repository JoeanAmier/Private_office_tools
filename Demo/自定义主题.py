import PySimpleGUI as sg

# Add your new theme colors and settings
my_new_theme = {'BACKGROUND': '#fef6e4',
                'TEXT': '#172c66',
                'INPUT': '#f3d2c1',
                'TEXT_INPUT': '#001858',
                'SCROLL': '#f582ae',
                'BUTTON': ('#232946', '#eebbc3'),
                'PROGRESS': ('#8bd3dd', '#f582ae'),
                'BORDER': 0,
                'SLIDER_DEPTH': 0,
                'PROGRESS_DEPTH': 0}

# Add your dictionary to the PySimpleGUI themes
sg.theme_add_new('MyNewTheme', my_new_theme)

# Switch your theme to use the newly added one. You can add spaces to make
# it more readable
sg.theme('My New Theme')

# Call a popup to show what the theme looks like
sg.popup_get_text('This how the MyNewTheme custom theme looks')
