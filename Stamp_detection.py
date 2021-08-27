import os
import time

import cv2
import fitz
import numpy as np

ZOOM = 0.1
MATRIX = fitz.Matrix(ZOOM, ZOOM)
ROOT = './cache/'
ERODE = np.ones((3, 3), np.uint8)
EXPAND = np.ones((4, 4), np.uint8)


def pdf_to_image(filename):
    doc = fitz.open(filename)
    for i in range(doc.page_count):
        page = doc[i]
        img = page.getPixmap(matrix=MATRIX, alpha=False)
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
    # view_image('处理前', img)
    height = img.shape[0]
    width = img.shape[1]
    for x in range(height):
        for y in range(width):
            if img[x, y, 0] <= 50 and img[x, y,
                                          1] <= 50 and img[x, y, 2] >= 200:
                modify_pixels(img, x, y, 0)
            else:
                modify_pixels(img, x, y, 255)
    # view_image('处理后', img)
    os.remove(file_1)
    os.remove(file_2)
    return stamp_ocr(img)


def view_image(arg0, img):
    cv2.imshow(arg0, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def modify_pixels(img, x, y, arg3):
    img[x, y, 0] = arg3
    img[x, y, 1] = arg3
    img[x, y, 2] = arg3


def stamp_ocr(img):
    img = cv2.blur(img, (2, 2))
    img = cv2.fastNlMeansDenoisingColored(img, None, 15, 15, 7, 21)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    erode = cv2.erode(gray, ERODE)
    expand = cv2.dilate(erode, EXPAND)
    # view_image('检测前图像', expand)
    circles = cv2.HoughCircles(
        expand,
        cv2.HOUGH_GRADIENT,
        1,
        10,
        param1=200,
        param2=10,
        minRadius=5,
        maxRadius=15)
    try:
        for _ in circles[0]:
            return True
        # print(len(circles[0]))
        # for circle in circles[0]:
        #     x = int(circle[0])
        #     y = int(circle[1])
        #     r = int(circle[2])
        #     img = cv2.circle(img, (x, y), r, (0, 0, 255), 2, 8, 0)
        # view_image('识别结果', img)
        # return True
    except TypeError:
        # print('识别圆形失败！')
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
    print('小工具版本号：0.0.5')
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
