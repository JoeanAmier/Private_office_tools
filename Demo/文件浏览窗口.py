import PySimpleGUI as sg

layout = [
    [sg.Button('选择文件', font=("微软雅黑", 12))]
]

win_1 = sg.Window('浏览文件', layout, size=(250, 100), )
while True:
    ev1, values_1 = win_1.read(timeout=100)
    if ev1 is None:
        break

    if ev1 == '选择文件':
        win_1.Hide()
        win_2 = sg.popup_get_file(
            '', file_types=(
                ('PDF', '*.pdf'),), no_window=True, multiple_files=True)
        print(win_2)
        win_1.un_hide()
