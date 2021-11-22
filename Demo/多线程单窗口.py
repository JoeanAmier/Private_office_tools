import threading
import time

import PySimpleGUI as sg


def sleep():
    time.sleep(5)
    global num
    print(f'任务{num}已完成')
    num += 1


layout = [[sg.Button('开始'), ],
          [sg.Text(size=(32, 2), key='A')],
          [sg.Button('重置'), sg.Button('退出')]]

win = sg.Window('窗口', layout)
thread = None
num = 0
while True:
    ev, values = win.read(timeout=50)
    if ev is None or ev == '退出':
        break

    elif ev == '开始':
        thread = threading.Thread(target=sleep)
        thread.start()

    elif ev == '重置':
        win['A'].update('重置')

    if thread:  # 加载动画
        sg.popup_animated(
            sg.DEFAULT_BASE64_LOADING_GIF,
            background_color='white',
            transparent_color='white',
            time_between_frames=50)
        thread.join(timeout=0)
        if not thread.is_alive():
            sg.popup_animated(None)
            thread = None
            win['A'].update(f'完成{num}次')

win.close()
