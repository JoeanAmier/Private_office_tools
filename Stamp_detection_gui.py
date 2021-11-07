import os
import webbrowser

import PySimpleGUI as sg
import cv2
import fitz
import numpy as np
import pandas as pd

MATRIX = fitz.Matrix(0.2, 0.2)
ROOT = './cache/'
LOWER_RED_1 = np.array([0, 5, 5])
UPPER_RED_1 = np.array([10, 255, 255])
LOWER_RED_2 = np.array([156, 5, 5])
UPPER_RED_2 = np.array([180, 255, 255])
EXPAND = np.ones((4, 4), np.uint8)
VERSION = 'V0.0.9'


class GUI:

    def __init__(self):
        sg.theme('GreenMono')
        window = self.home()
        if not os.path.exists(ROOT):
            os.mkdir(ROOT)
        else:
            window.find_element('status').update('程序异常，请删除“cache”文件夹后重新启动程序！')
        while True:
            event, values = window.read()
            if event is None:
                if not os.listdir(ROOT):
                    os.rmdir(ROOT)
                break
            elif event == '开始检测文件':
                if not values[0]:
                    window.find_element('status').update('未选择文件！')
                    continue
                self.deal(window, values['A'], values[0])
                window.find_element('status').update('当前选择文件检测完成！')
            elif event == 'all':
                self.deal(window, values['A'])
                window.find_element('status').update('当前目录全部 PDF 文件检测完成！')
            elif event == 'info':
                webbrowser.open(
                    'https://github.com/JoeanAmiee/Private_office_tools')

    @staticmethod
    def home():
        layout = [
            [sg.Text('选择文件：', font=('微软雅黑', 12)), sg.Input(font=('微软雅黑', 12)),
             sg.FileBrowse('浏览文件', font=('微软雅黑', 10), file_types=(".pdf PDF",), auto_size_button=True)],
            [sg.Radio('仅生成异常结果', group_id='0', default=True, font=('微软雅黑', 12)),
             sg.Radio('生成全部结果', group_id='0', key='A', font=('微软雅黑', 12))],
            [sg.Submit('开始检测文件', font=('微软雅黑', 12)),
             sg.Button('检测当前目录全部 PDF 文件', key='all', font=('微软雅黑', 12)),
             sg.Button('查看工具详细说明', key='info', font=('微软雅黑', 12))],
            [sg.StatusBar('准备就绪', key='status', font=('微软雅黑', 12), size=(10, 1))],
        ]
        return sg.Window(
            f'印章检测小工具 {VERSION}',
            layout,
            text_justification='center',
            element_justification='center',
            finalize=True)

    def deal(self, window, all_, file=None):
        window.Hide()
        wait = self.deal_gui()
        if not file:
            pdf = os.listdir()
            log = [check_pdf(i) for i in pdf if i.endswith('.pdf')]
        else:
            log = [check_pdf(file)]
        save_log(log, all_)
        wait.close()
        window.UnHide()

    @staticmethod
    def deal_gui():
        layout = [
            [sg.Text('正在检测文件状态，请耐心等待……', font=('微软雅黑', 12))],
        ]
        return sg.Window(
            '处理中',
            layout,
            text_justification='center',
            element_justification='center',
            finalize=True)


def pdf_to_image(filename):
    """PDF生成图片"""
    doc = fitz.open(filename)
    for i in range(doc.page_count):
        page = doc[i]
        img = page.get_pixmap(matrix=MATRIX, alpha=False)
        img.save(os.path.join(ROOT, "%s.png" % i))
    doc.close()


def deal_img(num):
    """提取红色部分"""
    file = os.path.join(ROOT, f'{num}.png')
    img = cv2.imdecode(np.fromfile(file, dtype=np.uint8), -1)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask_1 = cv2.inRange(img_hsv, LOWER_RED_1, UPPER_RED_1)
    mask_2 = cv2.inRange(img_hsv, LOWER_RED_2, UPPER_RED_2)
    mask = mask_1 + mask_2
    # print(sum(sum(i) for i in mask))  # 开发使用
    if sum(sum(i) for i in mask) < 250000:
        expand = cv2.dilate(mask, EXPAND)
        cv2.imwrite(file, expand)
    else:
        os.remove(file)
        # print(f'{num + 1}未生成图像！')  # 开发使用


def read_img(num):
    """识别文件"""
    file = os.path.join(ROOT, f'{num}.png')
    img = cv2.imread(file)
    if img is None:
        return None
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    os.remove(file)
    # return stamp_ocr_test(img, gray)  # 开发使用
    return stamp_ocr(gray)


def view_image(title, img):
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def modify_pixels(img, x, y, num):
    img[x, y, 0] = num
    img[x, y, 1] = num
    img[x, y, 2] = num


def stamp_ocr(img):
    """识别圆形"""
    circles = cv2.HoughCircles(
        img,
        cv2.HOUGH_GRADIENT,
        1,
        10,
        param1=200,
        param2=10,
        minRadius=8,
        maxRadius=16)
    try:
        for _ in circles[0]:
            return True
    except TypeError:
        return False


def stamp_ocr_test(img, gray):
    circles = cv2.HoughCircles(
        gray,
        cv2.HOUGH_GRADIENT,
        1,
        10,
        param1=200,
        param2=10,
        minRadius=8,
        maxRadius=16)
    try:
        print(f'检测到 {len(circles[0])} 个圆形！')
        for circle in circles[0]:
            x = int(circle[0])
            y = int(circle[1])
            r = int(circle[2])
            img = cv2.circle(img, (x, y), r, (0, 0, 255), 2, 8, 0)
        view_image('识别结果', img)
        return True
    except TypeError:
        print('识别圆形失败！')
        return False


def check_pdf(filename):
    pdf_to_image(filename)
    file = len(os.listdir(ROOT))
    [deal_img(i) for i in range(file)]
    result = [read_img(i) for i in range(file)]
    # print(f'{filename} 扫描完成！')
    return filename, result


def save_log(log, all_=False):
    for i, j in log:
        name, _ = os.path.splitext(i)
        data = [
            [x + 1, str(y)]
            for x, y in enumerate(j)
            if not all_ and y in [False, None] or all_
        ]
        if data:
            data = pd.DataFrame(data, columns=['页码', '状态'])
            data.to_excel(f'{name}.xlsx')


def main():
    GUI()


if __name__ == '__main__':
    main()
