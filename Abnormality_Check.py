import os
import webbrowser
from multiprocessing import Process
from multiprocessing import freeze_support

import PySimpleGUI as sg
import fitz
import pandas as pd
import pickle

ROOT = './img/'


class GUI:
    def __init__(self):
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
        if not os.path.exists(ROOT):
            os.mkdir(ROOT)
        else:
            self.main.find_element('status').update(
                '程序异常，请尝试删除“img”文件夹后重新启动程序！', text_color="red")
        while True:
            event, values = self.main.read(timeout=100)
            if event is None:
                break
            elif event == 'choice':
                self.choice_deal(values['low'])
            elif event == 'info':
                webbrowser.open(
                    'https://github.com/JoeanAmiee/Private_office_tools')
        self.main.close()
        if not os.listdir(ROOT):
            os.rmdir(ROOT)

    def home(self):
        layout = [
            [sg.Text('已检测且包含非正常页的文件（点击选中文件）：', font=('微软雅黑', 12))],
            [sg.Listbox(values=[], size=(80, 10), key='-FILE-')],
            [sg.Button('浏览文件', key='choice', font=('微软雅黑', 12), tooltip='选择 xlsx 格式的检测结果文件，并开始预览检查！'),
             sg.Button('检查文件', key='check', font=('微软雅黑', 12), tooltip='开始预览检查选中的 PDF 文件！'),
             sg.Button('查看工具详细说明', key='info', font=('微软雅黑', 12))],
            [sg.Checkbox('低性能模式', font=('微软雅黑', 10), key='low', pad=((480, 0), (0, 0)),
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

    @staticmethod
    def check_gui():
        layout = [
            [sg.Frame('', [
                [sg.Text('异常页：', font=('微软雅黑', 12)), ],
                [sg.Listbox(values=[], size=(10, 37), key='-PAGE-'), ],
            ], border_width=0, element_justification='center'),
             sg.Frame('', [
                 [sg.Text('预览：', font=('微软雅黑', 12)), ],
                 [sg.Image('', key='-IMAGE-', size=(440, 630))],
             ], border_width=0, element_justification='center')],
            [sg.Button('正常页', key='-TRUE-', font=('微软雅黑', 12), tooltip='标记当前页为正常页！'),
             sg.Button('异常页', key='-FALSE-', font=('微软雅黑', 12), tooltip='标记当前页为异常页！'),
             sg.Button('完成检查', key='-OVER-', font=('微软雅黑', 12), tooltip='保存检查结果！')],
        ]
        return sg.Window(
            '预览检查',
            layout,
            text_justification='center',
            element_justification='center',
            # icon=self.ICO,
            finalize=True)

    def start_check(self, xlsx, num):
        images = os.listdir(ROOT)
        pages = [i.replace(".png", "") for i in images]
        new_log = pages.copy()

        def update(gui, page, confirm=False):
            nonlocal pages, new_log
            pages.remove(page)
            if confirm:
                new_log.remove(page)
            if pages:
                gui['-PAGE-'].update(pages)
            else:
                gui['-PAGE-'].update(pages)
                gui['-IMAGE-'].update('')

        gui = self.check_gui()
        self.main.Hide()
        gui['-PAGE-'].update(values=pages)
        while True:
            event, values = gui.read(timeout=100)
            if not pages:
                break
            elif not values:
                break
            elif not values['-PAGE-']:
                continue
            cache = values["-PAGE-"][0]
            gui['-IMAGE-'].update(filename=f'./img/{cache}.png')
            if event is None:
                break
            elif event == '-TRUE-':
                update(gui, cache, True)
            elif event == '-FALSE-':
                update(gui, cache)
        self.main.UnHide()
        print(pages, new_log)
        gui.close()

    def choice_deal(self, save):
        file = self.choice_file()
        if file and '_正常' not in file:
            page = self.check_xlsx(file)
            if page:
                pdf = file.replace('xlsx', 'pdf')
                if os.path.exists(pdf):
                    # task = Process(
                    #     target=self.pdf_to_image, args=(pdf, page, save),
                    #     daemon=True)
                    # task.start()
                    # task.join()
                    self.start_check(file, page)
                else:
                    self.main.find_element('status').update('选择的文件所对应的 PDF 文件不存在！')
            else:
                self.main.find_element('status').update('选择的文件均为正常页，无需检查！')
        else:
            self.main.find_element('status').update('未选择文件，或选择的文件均为正常页，无需检查！')

    @staticmethod
    def pdf_to_image(filename, page_list, save):
        """PDF生成图片"""
        doc = fitz.open(filename)
        if save:
            for i in page_list:
                img = doc[i].get_pixmap(matrix=fitz.Matrix(0.7, 0.7), alpha=False)
                img.save(os.path.join(ROOT, "%s.png" % i))
                fitz.TOOLS.store_shrink(100)  # 清空缓存
        else:
            for i in page_list:
                img = doc[i].get_pixmap(matrix=fitz.Matrix(0.7, 0.7), alpha=False)
                img.save(os.path.join(ROOT, "%s.png" % i))
        doc.close()

    @staticmethod
    def check_xlsx(file):
        xlsx = pd.read_excel(file, usecols=['页码', '状态'], dtype={'页码': int, '状态': str})
        if xlsx.empty:
            return None
        xlsx = xlsx[(xlsx['状态'] == 'None') | (xlsx['状态'] == 'False')]
        xlsx = xlsx['页码'].tolist()
        return xlsx

    def choice_file(self):
        return sg.popup_get_file(
            '',
            file_types=(
                ('XLSX',
                 '*.xlsx'),
            ),
            # icon=self.ICO,
            no_window=True,
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
