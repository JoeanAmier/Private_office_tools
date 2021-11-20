import PySimpleGUI as sg

layout = [[sg.Text('输入文本'), ],
          [sg.Input(do_not_clear=True)],
          [sg.Text(size=(15, 1), key='A')],
          [sg.Button('窗口B'), sg.Button('退出')]]

win_1 = sg.Window('窗口A', layout)

win_2_active = False
while True:
    ev_1, values_1 = win_1.read(timeout=1000)
    win_1['A'].update(values_1[0])
    if ev_1 is None or ev_1 == '退出':
        break

    elif not win_2_active and ev_1 == '窗口B':
        win_2_active = True
        layout2 = [[sg.Text('输入文本'), ],
                   [sg.Input(do_not_clear=True)],
                   [sg.Button('退出')]]

        win_2 = sg.Window('窗口B', layout2)

    elif win_2_active:
        ev_2, values_2 = win_2.read(timeout=1000)
        if ev_2 is None or ev_2 == '退出':
            win_2_active = False
            win_2.close()
