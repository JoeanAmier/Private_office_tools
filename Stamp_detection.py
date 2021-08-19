import os
import time

import cv2
import fitz
import numpy as np

zoom = 0.2
mat = fitz.Matrix(zoom, zoom)
ROOT = './cache/'


def pdf_to_image(filename):
    doc = fitz.open(filename)
    for i in range(doc.page_count):
        page = doc[i]
        img = page.getPixmap(matrix=mat, alpha=False)
        img.writePNG(os.path.join(ROOT, "%s.png" % i))
    doc.close()


def deal_img(num):
    file = os.path.join(ROOT, f'{num}.png')
    img = cv2.imread(file)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(os.path.join(ROOT, f'{num}_g.png'), gray)


def read_img(num):
    file_1 = os.path.join(ROOT, f'{num}.png')
    file_2 = os.path.join(ROOT, f'{num}_g.png')
    img_1 = cv2.imread(file_1)
    img_2 = cv2.imread(file_2)
    img = img_2 - img_1
    # cv2.imshow('处理前', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    height = img.shape[0]
    width = img.shape[1]
    for x in range(height):
        for y in range(width):
            if img[x, y, 0] <= 50 and img[x, y,
                                          1] <= 50 and img[x, y, 2] >= 200:
                img[x, y, 0] = 0
                img[x, y, 1] = 0
                img[x, y, 2] = 0
            else:
                img[x, y, 0] = 255
                img[x, y, 1] = 255
                img[x, y, 2] = 255
    # cv2.imshow('处理后', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    os.remove(file_1)
    os.remove(file_2)
    return stamp_ocr(img)


def stamp_ocr(img):
    img = cv2.blur(img, (3, 3))
    img = cv2.fastNlMeansDenoisingColored(img, None, 15, 15, 7, 21)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((6, 6), np.uint8)
    erode = cv2.erode(gray, kernel)
    kernel = np.ones((3, 3), np.uint8)
    expand = cv2.dilate(erode, kernel)
    # cv2.imshow('5', expand)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    circles = cv2.HoughCircles(
        expand,
        cv2.HOUGH_GRADIENT,
        1,
        15,
        param1=200,
        param2=20,
        minRadius=5,
        maxRadius=35)
    try:
        for _ in circles[0]:
            return True
        # for circle in circles[0]:
        #     x = int(circle[0])
        #     y = int(circle[1])
        #     r = int(circle[2])
        #     img = cv2.circle(img, (x, y), r, (255, 0, 0), 2, 8, 0)
        # cv2.imshow('5', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # return True
    except TypeError:
        return False


def check_pdf(filename):
    pdf_to_image(filename)
    file = len(os.listdir(ROOT))
    [deal_img(i) for i in range(file)]
    result = [read_img(i) for i in range(file)]
    print(f'{filename} 扫描完成！')
    if all(result):
        return '%s：正常！' % filename
    cache = [str(i + 1) for i, j in enumerate(result) if not j]
    return f"{filename}：异常，页码：{','.join(cache)}！"


def save_log(log):
    with open('文件扫描结果.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(log))
        f.close()
    print('=' * 33)
    print('文件扫描结果已保存！')


def main():
    print('本程序自动获取当前目录 PDF 文件，并识别文件状态！')
    print('小工具版本号：0.0.4')
    print('=' * 33)
    start = time.time()
    if not os.path.exists(ROOT):
        os.mkdir(ROOT)
    pdf = os.listdir()
    log = [check_pdf(i) for i in pdf if i.endswith('.pdf')]
    save_log(log)
    os.rmdir(ROOT)
    print('处理耗时：{:.2f}s'.format(time.time() - start))
    print('程序运行结束，此窗口即将关闭！')
    time.sleep(10)


if __name__ == '__main__':
    main()
