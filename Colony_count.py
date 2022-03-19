from decimal import Decimal
from decimal import InvalidOperation
from itertools import chain

import pandas as pd

parameter = {
    '总数': ('菌落总数', '30', '300'),
    '霉酵': ('霉菌与酵母', '10', '150'),
    '金葡': ('金黄色葡萄球菌', '20', '200'),
    '李斯特': ('单核细胞增生李斯特氏菌', '15', '150'),
}


def total(item, low, high):
    data = []
    while True:
        cache = input('输入数据（梯度,菌落数,菌落数）：')
        cache = cache.replace(' ', '').split(',')
        if (n := len(cache)) == 1:
            break
        elif n == 3:
            try:
                cache[0] = int(cache[0])
                cache[1] = Decimal(cache[1])
                cache[2] = Decimal(cache[2])
            except (InvalidOperation, ValueError):
                print('输入数据内容错误！')
                continue
            if set(cache[1:]) == {Decimal('0')}:
                continue
            valid = False
            for i in cache[1:]:
                if Decimal(low) <= i <= Decimal(high):
                    valid = True
                    break
            data.append([valid] + cache)
        else:
            print('输入数据格式错误！')
            continue
    if not data:
        return
    data.sort(key=lambda x: x[1], reverse=True)
    print(pd.DataFrame(data, columns=['适宜计数', '稀释倍数', '菌落数一', '菌落数二']))
    if len(valid := [x for x in data if x[0]]) == 1:
        return f"{item}结果：{(valid[0][2] + valid[0][3]) / Decimal('2') / Decimal(str(10 ** valid[0][1]))}"
    elif len(valid) == 2:
        n_1 = [x for x in [valid[0][2], valid[0][3]]
               if Decimal(low) <= x <= Decimal(high)]
        n_2 = [x for x in [valid[1][2], valid[1][3]]
               if Decimal(low) <= x <= Decimal(high)]
        c = sum(n_1 + n_2)
        return f"{item}结果：{c / (Decimal(len(n_1)) + Decimal('0.1') * Decimal(len(n_2))) / Decimal(str(10 ** valid[0][1]))}"
    elif min(list(chain(*[[x[2], x[3]] for x in data]))) > Decimal(high):
        return f"{item}结果：{(data[-1][2] + data[-1][3]) / Decimal('2') / Decimal(str(10 ** data[-1][1]))}"
    elif max(list(chain(*[[x[2], x[3]] for x in data]))) < Decimal(low):
        return f"{item}结果：{(data[0][2] + data[0][3]) / Decimal('2') / Decimal(str(10 ** data[0][1]))}"
    else:
        cache = []
        for i in data:
            i = (i[2] + i[3]) / Decimal('2')
            i = min(abs(i - Decimal(low)), abs(i - Decimal(high)))
            cache.append(i)
        if len(cache) == len(set(cache)):
            i = cache.index(min(cache))
        else:
            cache = []
            for i in data:
                i = (i[2] + i[3]) / Decimal('2')
                i = min(abs(i - Decimal(low)) / Decimal(low),
                        abs(i - Decimal(high)) / Decimal(high))
                cache.append(i)
            i = cache.index(min(cache))
        return f"{item}结果：{(data[i][2] + data[i][3]) / Decimal('2') / Decimal(str(10 ** data[i][1]))}"


def three(item, low, high):
    def formula(data):
        return f"{item}结果：{data[0][5] * data[0][6] / data[0][7] / Decimal(str(10 ** data[0][1]))}"

    data = []
    while True:
        cache = input('输入数据（梯度,菌落数,菌落数,菌落数,阳性菌落数,鉴定菌落数）：')
        cache = cache.replace(' ', '').split(',')
        if (n := len(cache)) == 1:
            break
        elif n == 6:
            try:
                cache[0] = int(cache[0])
                cache[1] = Decimal(cache[1])
                cache[2] = Decimal(cache[2])
                cache[3] = Decimal(cache[3])
                cache[4] = Decimal(cache[4])
                cache[5] = Decimal(cache[5])
            except (InvalidOperation, ValueError):
                print('输入数据内容错误！')
                continue
            if set(cache[1:4]) == {Decimal('0')}:
                continue
            all_ = sum(cache[1:4])
            valid = True if Decimal(low) <= all_ <= Decimal(high) else False
            data.append([valid] + cache[:4] + [all_] + cache[4:])
        else:
            print('输入数据格式错误！')
            continue
    if not data:
        return
    data.sort(key=lambda x: x[1], reverse=True)
    print(
        pd.DataFrame(
            data,
            columns=[
                '适宜计数',
                '稀释倍数',
                '菌落数一',
                '菌落数二',
                '菌落数三',
                '典型菌落总数',
                '阳性菌落数',
                '鉴定菌落数']))
    if len(valid := [x for x in data if x[0]]) == 1:
        return formula(valid)
    elif data[0][5] < Decimal(low):
        return formula(data[0])
    elif max_ := (max([x[5] for x in data])) > Decimal(high):
        cache = [x[5] for x in data]
        i = cache.index(max_)
        if i == len(data) - 1 or data[i + 1][5] == Decimal('0'):
            return formula(data[i])
        return formula(data[i + 1])
    elif len(valid) == 2:
        one = valid[0][5] * valid[0][6] / valid[0][7]
        two = valid[1][5] * valid[1][6] / valid[1][7]
        return f"{item}结果：{one + two / Decimal('1.1') / valid[0][1]}"
    else:
        return '未知情况！'


def double(item='大肠菌群'):
    data = input('输入数据（梯度,菌落数,菌落数,阳性管,鉴定菌落数）：')
    data = data.replace(' ', '').split(',')
    if len(data) == 5:
        try:
            data[0] = int(data[0])
            data[1] = Decimal(data[1])
            data[2] = Decimal(data[2])
            data[3] = Decimal(data[3])
            data[4] = Decimal(data[4])
        except (InvalidOperation, ValueError):
            print('输入数据内容错误！')
            return
    else:
        print('输入数据格式错误！')
        return
    print(pd.Series(data, index=['稀释倍数', '菌落数一', '菌落数二', '阳性管', '鉴定菌落数']))
    return f"{item}结果：{(data[1] + data[2]) / Decimal('2') * data[3] / data[4] / Decimal(str(10 ** data[0]))}"


if __name__ == '__main__':
    print(total(*parameter['总数']))
    # print(total(*parameter['霉酵']))
    # print(three(*parameter['金葡']))
    # print(three(*parameter['李斯特']))
    # print(double())  # 大肠菌群
