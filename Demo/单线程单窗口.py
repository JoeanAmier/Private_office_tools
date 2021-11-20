import PySimpleGUI as sg

layout = [[sg.Text('输入文本'), ],
          [sg.Input(do_not_clear=True)],
          [sg.Text(size=(15, 1), key='A')],
          [sg.Button('窗口B')]]

win_1 = sg.Window('窗口A', layout)
win_2_active = False
while True:
    ev1, values_1 = win_1.read(timeout=1000)
    if ev1 is None:
        break
    win_1['A'].update(values_1[0])

    if ev1 == '窗口B' and not win_2_active:
        win_2_active = True
        win_1.Hide()
        layout2 = [[sg.Text('窗口B')],
                   [sg.Button('退出')]]

        win_2 = sg.Window('窗口B', layout2)
        while True:
            ev2, values_2 = win_2.read()
            if ev2 is None or ev2 == '退出':
                win_2.close()
                win_2_active = False
                win_1.UnHide()
                break
