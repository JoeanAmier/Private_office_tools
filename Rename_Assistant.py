import os
import webbrowser

import PySimpleGUI as sg


def delete_text(
        folder,
        first_num=0,
        last_num=None,
        format_=None,
        re_=None,
        run=False):
    """重命名：删除文本"""
    files = format_filtering(folder, format_)
    modify = [i[first_num:last_num] for i in files]
    if not run:
        return modify


def format_filtering(folder, format_=None):
    """获取文件夹内指定格式的文件"""
    files = os.listdir(folder)
    if format_:
        values = []
        for i in format_.split(';'):
            for j in files:
                if j.endswith(i):
                    values.append(j)
        return values
    return files


class GUI:
    # theme = {'BACKGROUND': '#fef6e4',
    #          'TEXT': '#172c66',
    #          'INPUT': '#f3d2c1',
    #          'TEXT_INPUT': '#001858',
    #          'SCROLL': '#f582ae',
    #          'BUTTON': ('#232946', '#eebbc3'),
    #          'PROGRESS': ('#8bd3dd', '#f582ae'),
    #          'BORDER': 0,
    #          'SLIDER_DEPTH': 0,
    #          'PROGRESS_DEPTH': 0}
    # sg.theme_add_new('RA_Theme', theme)
    # sg.theme('RA_Theme')
    version = 'V0.0.1'

    def __init__(self):
        self.main = self.home()
        self.files = None
        self.modify = None
        self.folder = None

    def home(self):
        before = [[sg.Text('处理前：')], [sg.Multiline(
            '', autoscroll=True, size=(32, 10), disabled=True, key='-BEFORE-')]]
        after = [[sg.Text('处理后：')], [sg.Multiline(
            '', autoscroll=True, size=(32, 10), disabled=True, key='-AFTER-')]]
        layout = [
            [sg.Frame('', before, element_justification='center', ),
             sg.Frame('', after, element_justification='center', )],
            [sg.Input(size=(60, 1), key='-SHOW-', tooltip='输入文件夹路径，或者点击右侧按钮选择文件夹！'),
             sg.Button('选择文件夹', key='-SELECT-')],
            [sg.Text('文件类型：'),
             sg.Input(size=(18, 1), key='-FORMAT-',
                      tooltip='如果需要重命名指定类型的文件，请输入文件类型！\n多种文件类型请使用英文分号隔开！\n例如：xlsx;xls;pdf'),
             sg.Button('应用')],
            [sg.TabGroup([[
                sg.Tab('主界面', self.about(), element_justification='center', ),
                sg.Tab('删除文本', self.delete_text_tab(), element_justification='center', ),
            ]])]]
        return sg.Window(
            f'文件重命名小工具 {self.version}',
            layout,
            font=('微软雅黑', 11),
            element_justification='center',
            # icon=self.ICO,
            finalize=True)

    @staticmethod
    def about():
        return [
            [sg.Text('文件重命名小工具：'), ],
            [sg.Text('批量删除文件名称指定部分'), ],
            [sg.Button('访问网站', key='-INFO-'), ],
        ]

    @staticmethod
    def delete_text_tab():
        setup = [
            [sg.Text('起始文本序号：'), sg.Input(size=(6, 1), key='-DT_F_INDEX-'),
             sg.Text('结束文本序号：'), sg.Input(size=(6, 1), key='-DT_L_INDEX-'), ],
            [sg.Text('正则表达式匹配：'), sg.Input('暂不支持', size=(54, 1), disabled=True)],
            [sg.Button('开始处理')]
        ]
        return [
            [sg.Frame('', setup, element_justification='center')],
        ]

    def run(self):
        while True:
            event, values = self.main.read(timeout=100)
            if event is None:
                break
            elif event == '-SELECT-':
                if file := self.choice_file():
                    self.folder = file
                    self.files = os.listdir(self.folder)
                    self.main['-SHOW-'].update(self.folder)
                    self.main['-BEFORE-'].update('\n'.join(self.files))
                # 判断格式输入框有没有修改，有的话进行更新
                # 多线程更新预览
            elif event == '-INFO-':
                webbrowser.open(
                    'https://github.com/JoeanAmiee/Private_office_tools')
        self.main.close()

    def choice_file(self):
        return sg.popup_get_folder(
            '',
            # icon=self.ICO,
            no_window=True,
        )


def main():
    GUI().run()


if __name__ == '__main__':
    main()
