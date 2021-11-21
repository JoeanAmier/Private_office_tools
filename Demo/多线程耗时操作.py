import threading
import time

import PySimpleGUI as sg


def long_function_thread(window):
    time.sleep(10)
    window.write_event_value('-THREAD DONE-', '')


def long_function():
    threading.Thread(
        target=long_function_thread, args=(
            window,), daemon=True).start()


layout = [[sg.Output(size=(60, 10))],
          [sg.Button('Go'), sg.Button('Nothing'), sg.Button('Exit')]]

window = sg.Window('Window Title', layout)

while True:  # Event Loop
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Go':
        print('About to go to call my long function')
        long_function()
        print('Long function has returned from starting')
    elif event == '-THREAD DONE-':
        print('Your long operation completed')
    else:
        print(event, values)
window.close()
