import os
import time

import cv2
import fitz
import numpy as np

MATRIX = fitz.Matrix(0.2, 0.2)
ROOT = './cache/'
LOWER_RED_1 = np.array([0, 5, 5])
UPPER_RED_1 = np.array([10, 255, 255])
LOWER_RED_2 = np.array([156, 5, 5])
UPPER_RED_2 = np.array([180, 255, 255])
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
    img = cv2.imdecode(np.fromfile(file, dtype=np.uint8), -1)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask_1 = cv2.inRange(img_hsv, LOWER_RED_1, UPPER_RED_1)
    mask_2 = cv2.inRange(img_hsv, LOWER_RED_2, UPPER_RED_2)
    mask = mask_1 + mask_2
    # print(sum(sum(i) for i in mask))
    if sum(sum(i) for i in mask) < 200000:
        expand = cv2.dilate(mask, EXPAND)
        cv2.imwrite(file, expand)
    else:
        os.remove(file)
        # print(f'{num + 1}未生成图像！')


def read_img(num):
    file = os.path.join(ROOT, f'{num}.png')
    img = cv2.imread(file)
    if img is None:
        return False
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    os.remove(file)
    # return stamp_ocr_test(img, gray)
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
    print('本程序自动获取当前目录全部 PDF 文件，并识别文件状态！')
    print('小工具版本号：0.0.7 Beta')
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
