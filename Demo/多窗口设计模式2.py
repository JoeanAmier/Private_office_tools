import PySimpleGUI as sg

layout = [[sg.Text('Window 1'), ],
          [sg.Input(do_not_clear=True)],
          [sg.Text(size=(15, 1), key='-OUTPUT-')],
          [sg.Button('Launch 2')]]

win_1 = sg.Window('Window 1', layout)
win_2_active = False
while True:
    ev1, values_1 = win_1.read(timeout=100)
    if ev1 is None:
        break
    win_1.FindElement('-OUTPUT-').update(values_1[0])

    if ev1 == 'Launch 2' and not win_2_active:
        win_2_active = True
        win_1.Hide()
        layout2 = [[sg.Text('Window 2')],
                   [sg.Button('Exit')]]

        win_2 = sg.Window('Window 2', layout2)
        while True:
            ev2, values_2 = win_2.read()
            if ev2 is None or ev2 == 'Exit':
                win_2.close()
                win_2_active = False
                win_1.UnHide()
                break
