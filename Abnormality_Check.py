import os
import webbrowser
from multiprocessing import Process
from multiprocessing import freeze_support

import PySimpleGUI as sg
import fitz
import numpy as np
import pandas as pd
import pickle


class GUI:
    def __init__(self):
        self.root = './img/'
        self.version = 'V0.0.1'
        self.log = None
        self.set_theme()
        self.main = self.home()

    @staticmethod
    def set_theme():
        theme = {'BACKGROUND': '#fef6e4',
                 'TEXT': '#172c66',
                 'INPUT': '#f3d2c1',
                 'TEXT_INPUT': '#001858',
                 'SCROLL': '#f582ae',
                 'BUTTON': ('#232946', '#eebbc3'),
                 'PROGRESS': ('#8bd3dd', '#f582ae'),
                 'BORDER': 0,
                 'SLIDER_DEPTH': 0,
                 'PROGRESS_DEPTH': 0}
        sg.theme_add_new('RE_Theme', theme)
        sg.theme('RE_Theme')

    def run(self):
        if not os.path.exists(self.root):
            os.mkdir(self.root)
        else:
            self.main.find_element('status').update(
                '程序异常，请尝试删除“img”文件夹后重新启动程序！', text_color="red")
        while True:
            event, values = self.main.read(timeout=100)
            if event is None:
                break
            elif event == 'choice':
                self.main['choice'].update(disabled=True)
                cache = self.choice_file()
                self.main['choice'].update(disabled=False)
            elif event == 'scan':
                self.log = self.get_log()
            elif event == 'info':
                webbrowser.open(
                    'https://github.com/JoeanAmiee/Private_office_tools')
        self.main.close()
        if not os.listdir(self.root):
            os.rmdir(self.root)

    def home(self):
        layout = [
            [sg.Multiline('Tips: 将鼠标悬停在按钮上可查看相应提示！',
                          autoscroll=True, font=('微软雅黑', 10), size=(68, 8), disabled=True,
                          key='screen')],
            [sg.Button('手动选择文件', key='choice', font=('微软雅黑', 12), tooltip='手动选择 xlsx 格式的检测结果文件！'),
             sg.Button('读取检测记录', key='scan', font=('微软雅黑', 12), tooltip='读取已检测的记录'),
             sg.Button('查看工具详细说明', key='info', font=('微软雅黑', 12))],
            [sg.Checkbox('低性能模式', font=('微软雅黑', 10), key='low', pad=((475, 0), (0, 0)),
                         tooltip='减少程序占用内存，但是会增加检测文件所用的时间\n建议低配置电脑或处理大文件时启用')],
            [sg.StatusBar('准备就绪', key='status', font=('微软雅黑', 12), size=(10, 1))],
        ]
        return sg.Window(
            f'异常页面检查辅助工具 {self.version}',
            layout,
            text_justification='center',
            element_justification='center',
            # icon=self.ICO,
            finalize=True)

    def choice_file(self):
        return sg.popup_get_file(
            '',
            file_types=(
                ('XLSX',
                 '*.xlsx'),
            ),
            # icon=self.ICO,
            no_window=True,
            multiple_files=True,
        )

    @staticmethod
    def get_log():
        if not os.path.exists('Inspection_records.pkl'):
            return None
        with open('Inspection_records.pkl', 'rb') as f:
            log = pickle.load(f)
        return log

    def finished(self):
        with open('Inspection_records.pkl', 'wb') as f:
            pickle.dump(self.log, f)


def main():
    GUI().run()


if __name__ == '__main__':
    freeze_support()
    main()
