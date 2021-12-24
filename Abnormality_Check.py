import os
import pickle
import webbrowser
from multiprocessing import Process
from multiprocessing import freeze_support

import PySimpleGUI as sg
import fitz
import pandas as pd

ROOT = './img/'


class GUI:
    def __init__(self):
        self.version = 'V0.1.0'
        self.set_theme()
        self.log = self.welcome()
        self.main = self.home()
        self.task = None
        self.file = None
        self.page = None
        self.pdf = None

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
        sg.theme_add_new('AC_Theme', theme)
        sg.theme('AC_Theme')

    def welcome(self):
        layout = [[sg.Text('正在扫描检测记录......\n请稍等......', font=('微软雅黑', 12))], ]
        gui = sg.Window(
            f'异常页面检查辅助工具 {self.version}',
            layout,
            size=(345, 70),
            text_justification='center',
            element_justification='center',
            # icon=self.ICO,
            finalize=True)
        log = self.check_log()
        gui.close()
        return log

    def run(self):
        if not os.path.exists(ROOT):
            os.mkdir(ROOT)
        else:
            self.main.find_element('status').update(
                '程序异常，请尝试删除“img”文件夹后重新启动程序！', text_color="red")
        self.main['-FILE-'].update(self.log)
        while True:
            event, values = self.main.read(timeout=100)
            if event is None:
                break
            elif event == 'choice':
                tip = self.choice_deal()
                if tip:
                    self.main.find_element('status').update(tip)
                    continue
                self.task = Process(target=self.pdf_to_image, args=(
                    self.pdf, self.page, values['low']), daemon=True)
                self.task.start()
            elif event == 'info':
                webbrowser.open(
                    'https://github.com/JoeanAmiee/Private_office_tools')
            if self.task:
                sg.popup_animated(
                    sg.DEFAULT_BASE64_LOADING_GIF,
                    message='处理中',
                    text_color='black',
                    font=('黑体', 12),
                    # icon=self.ICO,
                    background_color='white',
                    transparent_color='white',
                    time_between_frames=100)
                self.task.join(timeout=0)
                if not self.task.is_alive():
                    sg.popup_animated(None)
                    self.start_check(self.file, self.page)
                    self.task = None
                    self.file = None
                    self.page = None
                    self.pdf = None
        self.main.close()
        if not os.listdir(ROOT):
            os.rmdir(ROOT)
        self.finished()

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
                [sg.Listbox(values=[], size=(10, 35), key='-PAGE-'), ],
            ], border_width=0, element_justification='center'),
             sg.Frame('', [
                 [sg.Text('当前页：', font=('微软雅黑', 12)), sg.Text('', key='-NOW-', font=('微软雅黑', 12))],
                 [sg.Image('', key='-IMAGE-', size=(420, 590))],
             ], border_width=0, element_justification='center')],
            [sg.Button('正常页', key='-TRUE-', font=('微软雅黑', 12), tooltip='标记当前页为正常页！'),
             sg.Button('异常页', key='-FALSE-', font=('微软雅黑', 12), tooltip='标记当前页为异常页！'),
             sg.Button('保存结果', key='-OVER-', font=('微软雅黑', 12), tooltip='保存检查结果至 xlsx 文件！')],
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
        images = [os.path.join(ROOT, i) for i in images]
        remove = []

        def update(_gui, confirm=False):
            nonlocal images, pages, remove
            if confirm:
                remove.append(_gui['-NOW-'].DisplayText)
            os.remove(f"./img/{_gui['-NOW-'].DisplayText}.png")
            if len(pages) != 0:
                _gui['-NOW-'].update(pages.pop())
                _gui['-IMAGE-'].update(images.pop())
            else:
                _gui['-TRUE-'].update(disabled=True)
                _gui['-FALSE-'].update(disabled=True)

        gui = self.check_gui()
        self.main.Hide()
        gui['-PAGE-'].update(values=pages)
        gui['-PAGE-'].update(disabled=True)  # 暂时禁用
        images.reverse()
        pages.reverse()
        gui['-NOW-'].update(pages.pop())
        gui['-IMAGE-'].update(images.pop())
        while True:
            event, values = gui.read(timeout=100)
            if not event:
                break
            elif event == '-TRUE-':
                update(gui, True)
            elif event == '-FALSE-':
                update(gui)
            elif event == '-OVER-':
                self.update_log(remove)
                break
        self.main.UnHide()
        [os.remove(os.path.join(ROOT, i)) for i in os.listdir(ROOT)]
        gui.close()

    def update_log(self, sure):
        if sure:
            xlsx = self.check_xlsx(self.file, to=False)
            xlsx.drop([int(i) for i in sure], inplace=True)
            if xlsx.empty:
                self.log.discard(self.pdf)
            xlsx.to_excel(self.file)

    def choice_deal(self):
        self.file = self.choice_file().replace('/', '\\')
        if self.file and '_正常' not in self.file:
            self.page = self.check_xlsx(self.file)
            if self.page:
                self.pdf = self.file.replace('xlsx', 'pdf')
                if os.path.exists(self.pdf):
                    return None
                return '选择的文件所对应的 PDF 文件不存在！'
            return '选择的文件均为正常页，无需检查！'
        return '未选择文件，或者选择的文件均为正常页，无需检查！'

    @staticmethod
    def pdf_to_image(filename, page_list, save):
        """PDF生成图片"""
        doc = fitz.open(filename)
        if save:
            for i in page_list:
                img = doc[i -
                          1].get_pixmap(matrix=fitz.Matrix(0.7, 0.7), alpha=False)
                img.save(os.path.join(ROOT, "%s.png" % i))
                fitz.TOOLS.store_shrink(100)  # 清空缓存
        else:
            for i in page_list:
                img = doc[i -
                          1].get_pixmap(matrix=fitz.Matrix(0.7, 0.7), alpha=False)
                img.save(os.path.join(ROOT, "%s.png" % i))
        doc.close()

    @staticmethod
    def check_xlsx(file, to=True):
        xlsx = pd.read_excel(file, index_col=0, dtype={'状态': str})
        if xlsx.empty:
            return None
        xlsx = xlsx[(xlsx['状态'] == 'None') | (xlsx['状态'] == 'False')]
        if to:
            return xlsx.index.tolist()
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

    def check_log(self):
        log = self.get_log()
        if not log:
            return None
        new_ = set()
        for i in log:
            j = i.replace('.pdf', '.xlsx')
            if os.path.exists(j) and self.check_xlsx(j):
                new_.add(i)
        return new_

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
