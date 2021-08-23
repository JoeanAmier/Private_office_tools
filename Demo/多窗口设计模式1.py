import PySimpleGUI as sg

layout = [[sg.Text('Window 1'), ],
          [sg.Input(do_not_clear=True)],
          [sg.Text(size=(15, 1), key='-OUTPUT-')],
          [sg.Button('Launch 2'), sg.Button('Exit')]]

win_1 = sg.Window('Window 1', layout)

win_2_active = False
while True:
    ev_1, values_1 = win_1.read(timeout=100)
    win_1['-OUTPUT-'].update(values_1[0])
    if ev_1 is None or ev_1 == 'Exit':
        break

    if not win_2_active and ev_1 == 'Launch 2':
        win_2_active = True
        layout2 = [[sg.Text('Window 2')],
                   [sg.Button('Exit')]]

        win_2 = sg.Window('Window 2', layout2)

    if win_2_active:
        ev_2, values_2 = win_2.read(timeout=100)
        if ev_2 is None or ev_2 == 'Exit':
            win_2_active = False
            win_2.close()
