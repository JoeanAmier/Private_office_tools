import os
import time

import fitz
from skimage.io import imread

zoom = 1
mat = fitz.Matrix(zoom, zoom)
ROOT = os.getcwd() + '\\cache\\'


def pdf_to_image(filename):
    doc = fitz.open(filename)
    for i in range(doc.page_count):
        page = doc[i]
        img = page.getPixmap(matrix=mat, alpha=False)
        img.writePNG(os.path.join(ROOT, "%s.png" % i))
    doc.close()


def read_img(file):
    cache = os.path.join(ROOT, file)
    img = imread(cache)
    height = img.shape[0]
    width = img.shape[1]
    all_ = 0
    for i in range(height):
        for j in range(width):
            if img[i, j, 0] <= 140:
                continue
            if img[i, j, 1] >= 135:
                continue
            if img[i, j, 2] >= 125:
                continue
            all_ += 1
    os.remove(cache)
    # print(all_)  # 调试使用
    return all_ > 10


def get_file(filename):
    file = os.listdir(ROOT)
    result = [read_img(i) for i in file]
    print(f'{filename} 扫描完成！')
    if all(result):
        return '%s：正常！' % filename
    cache = [str(i + 1) for i, j in enumerate(result) if not j]
    return f"{filename}：异常，页码{','.join(cache)}！"


def check_pdf(filename):
    pdf_to_image(filename)
    return get_file(filename)


def save_log(log):
    with open('文件扫描结果.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(log))
        f.close()
    print('=' * 33)
    print('文件扫描结果已保存！')


def main():
    print('本程序自动获取当前目录 PDF 文件，并识别文件状态！')
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
