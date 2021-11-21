import time

import PySimpleGUI as sg

layout = [[sg.Button('开始'), ],
          [sg.Text(size=(32, 2), key='A')],
          [sg.Button('窗口B'), sg.Button('退出')]]

win_1 = sg.Window('窗口A', layout)

win_2_active = False
while True:
    ev_1, values_1 = win_1.read(timeout=100)
    if ev_1 is None or ev_1 == '退出':
        break

    elif ev_1 == '开始':
        for cache, _ in enumerate(range(10), start=1):
            time.sleep(1)
            win_1['A'].update(cache)
        cache = 0

    elif not win_2_active and ev_1 == '窗口B':
        win_2_active = True
        layout2 = [[sg.Button('开始'), ],
                   [sg.Text(size=(32, 2), key='B')],
                   [sg.Button('退出')]]

        win_2 = sg.Window('窗口B', layout2)

    elif win_2_active:
        ev_2, values_2 = win_2.read(timeout=100)
        if ev_2 is None or ev_2 == '退出':
            win_2_active = False
            win_2.close()
        elif ev_2 == '开始':
            for cache, _ in enumerate(range(10), start=1):
                time.sleep(1)
                win_2['B'].update(cache)
            cache = 0
