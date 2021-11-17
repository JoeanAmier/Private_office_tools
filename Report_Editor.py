import decimal
import webbrowser

import PySimpleGUI as sg
import pyperclip

TEXT = {
    '00': '△：n：同一批次产品应采集的样品件数，c：最大可允许超出m值的样品件数，m：微生物指标可接受水平的限量值，M：微生物指标的最高安全限值。',
    '01': '酒精度实测值与标签标示值允许差为±1.0%vol（标签标示值：XX%vol）',
    '02': 'α-666：0.0001\nβ-666：0.0004\nγ-666：0.0002\nδ-666：0.0001',
    '03': 'p,p’-DDE：0.0001\no,p’-DDE：0.0002\no,p’-DDD：0.0004\np,p’-DDT：0.0009',
    '04': 'α-六六六：\n0.000097\nβ-六六六：\n0.000634\nγ-六六六：\n0.000226\nδ-六六六：\n0.000179',
    '05': 'P,P’-滴滴伊：\n0.000345\nO,P’-滴滴涕：\n0.000412\nP,P’-滴滴滴：\n0.000465\nP,P’-滴滴涕：\n0.000481',
    '06': '标签审核内容不包括标示内容真实性和规范性的核实。',
    '07': '标签审核内容不包括标示内容真实性和规范性的核实。\n该样品为散装称重食品，参照GB 7718-2011、GB 28050-2011的要求进行审核，审核内容不包括净含量和规格。',
    '08': '标签审核内容不包括标示内容真实性的核实。',
    '09': '样品为电子标签，标签审核内容不包括强制标示内容的字符高度以及生产日期格式，以实物印刷为准。\n标签审核内容不包括标示内容真实性的核实。',
    '10': '样品为电子标签，标签审核内容不包括强制标示内容的字符高度以及生产日期格式，以实物印刷为准。\n标签审核内容不包括标示内容真实性的核实。\n本报告用于发证检验，食品生产许可证编号不在本次标签审核范围内。',
    '11': '样品为电子标签，标签审核内容不包括强制标示内容的字符高度以及生产日期格式，以实物印刷为准。\n标签审核内容不包括标示内容真实性的核实。\n该样品为散装称重食品，参照GB 7718-2011、'
          'GB 28050-2011的要求进行审核，审核内容不包括净含量和规格。',
    '12': '标签审核内容不包括标示内容真实性的核实。\n该样品为散装称重食品，参照GB 7718-2011、GB 28050-2011的要求进行审核，审核内容不包括净含量和规格。',
    '13': '样品为样版标签，标签审核内容不包括生产日期字符高度及格式，以实物印刷为准。\n标签审核内容不包括标示内容真实性的核实。',
    '14': '经抽样检验，所检项目序号“XXX”无限量要求，不作判定，所检其余项目',
    '15': '本报告代替编号为XXX的检测报告，原报告作废。',
    '16': '该阳性样品验证结果：不一致。',
    '17': '多氯联苯以 PCB28、PCB52、PCB101、PCB118、PCB138、PCB153 和 PCB180 总和计。',
    '18': '实测值为总汞。',
    '19': '定量限：\nα-六六六：\n0.01\nβ-六六六：\n0.01\nγ-六六六：\n0.05\nδ-六六六：\n0.01',
    '20': '标签审核结果详见第3页。',
}

LIMIT = {
    '香菇': ('91.7', '', '1', '0.5', '0.5', '0.1', '0'),
    '鲜枣': ('67.4', '', '0.1', '0', '0.05', '0', '0'),
    '葡萄': ('88.5', '', '0.2', '0', '0.05', '0', '0'),
    '木耳': ('91.8', '', '1', '0.5', '0.2', '0.1', '0'),
    '大白菜': ('94.4', '', '0.3', '0.5', '0.2', '0.01', '0'),
    '黄花菜': ('40.3', '', '0.1', '0.5', '0.2', '0.01', '0'),
    '芥菜': ('91.5', '', '0.3', '0.5', '0.2', '0.01', '0'),
    '豆角': ('90.0', '', '0.2', '0.5', '0.1', '0.01', '0'),
    '鲢鱼': ('77.4', '', '0.5', '0', '0.1', '0', '0'),
    '青鳞鱼': ('73.9', '', '0.5', '0', '0.1', '0', '0'),
    '鱿鱼': ('80.4', '', '1.0', '0', '0.1', '0', '0'),
    '柠檬': ('91.0', '', '0.1', '0', '0', '0', '0'),
    '柚': ('89.0', '', '0.1', '0', '0', '0', '0'),
    '西柚': ('90.9', '', '0.1', '0', '0', '0', '0'),
    '猪肉': ('71.0', '', '0.2', '0', '0.1', '0', '1'),
    '食用菌': ('', '', '1', '0.5', '0.2', '0.1', '0'),
}

SOLID = {
    '饮料': ('0', '0.5', '0.05', '0.1', '0'),
    '果蔬汁': ('1.0', '0.5', '0.05', '0.1', '0.05'),
    '含乳': ('0', '0.5', '0', '0.1', '0.05'),
    '植物蛋白': ('1.0', '0.5', '0', '0.1', '0.025'),
    '碳酸': ('0.2', '0.5', '0.05', '0.1', '0.05'),
    '风味': ('1.0', '0.5', '0', '0.1', '0'),
    '果味': ('1.0', '0.5', '0.05', '0.1', '0.05'),
}

SOLID_ITEMS = (
    None,
    None,
    '苯甲酸及其钠盐(以苯甲酸计)',
    '山梨酸及其钾盐(以山梨酸计)',
    '苋菜红',
    '柠檬黄',
    '胭脂红')
DEHYDRATION_ITEMS = (
    None,
    None,
    '铅(以Pb计)',
    '总砷(以As计)',
    '镉(以Cd计)',
    '总汞(以Hg计)',
    '铬(以Cr计)')


def valid_numbers(text, min_=False):
    if text.endswith('.0'):
        return '.0'
    elif text.endswith('.00'):
        return '.00'
    elif text.endswith('.000'):
        return '.000'
    text = text.lstrip('0')
    text = text.rstrip('0')
    if '.' not in text:
        return {True: '.0', False: '1.'}[min_]
    length = len(text[text.index('.') + 1:])
    length = min(length, 4)
    return '.' + '0' * length


def home():
    layout = [
        [sg.Button('营养成分表(基础)', size=(16, 2), font=('微软雅黑', 12)),
         sg.Button('营养成分表(详细)', size=(16, 2), font=('微软雅黑', 12))],
        [sg.Button('脱水率及限值计算', size=(16, 2), font=('微软雅黑', 12)),
         sg.Button('固体饮料限值计算', size=(16, 2), font=('微软雅黑', 12))],
        [sg.Button('常用文本剪贴板', size=(16, 2), font=('微软雅黑', 12)),
         sg.Button('查看工具详细说明', size=(16, 2), font=('微软雅黑', 12))],
    ]
    return sg.Window(
        '报告编辑部小工具 V0.0.8',
        layout,
        size=(
            405,
            210),
        text_justification='center',
        element_justification='center',
        finalize=True)


def nutrition_win():
    rc_11 = [
        [sg.Text('能量', font=('微软雅黑', 12))],
        [sg.Text('蛋白质', font=('微软雅黑', 12))],
        [sg.Text('脂肪', font=('微软雅黑', 12))],
        [sg.Text('碳水化合物', font=('微软雅黑', 12))],
        [sg.Text('钠', font=('微软雅黑', 12))],
    ]
    rc_12 = [
        [sg.Input(key='00', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Input(key='01', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Input(key='02', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Input(key='03', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Input(key='04', size=(10, 1), font=('微软雅黑', 12))],
    ]
    rc_13 = [
        [sg.Text(key='10', size=(5, 1), font=('微软雅黑', 12))],
        [sg.Text(key='11', size=(5, 1), font=('微软雅黑', 12))],
        [sg.Text(key='12', size=(5, 1), font=('微软雅黑', 12))],
        [sg.Text(key='13', size=(5, 1), font=('微软雅黑', 12))],
        [sg.Text(key='14', size=(5, 1), font=('微软雅黑', 12))],
    ]
    rc_14 = [
        [sg.Text(key='20', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='21', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='22', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='23', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='24', size=(10, 1), font=('微软雅黑', 12))],
    ]
    rc_15 = [
        [sg.Text(key='30', size=(5, 1), font=('微软雅黑', 12))],
        [sg.Text(key='31', size=(5, 1), font=('微软雅黑', 12))],
        [sg.Text(key='32', size=(5, 1), font=('微软雅黑', 12))],
        [sg.Text(key='33', size=(5, 1), font=('微软雅黑', 12))],
        [sg.Text(key='34', size=(5, 1), font=('微软雅黑', 12))],
    ]
    rc_16 = [
        [sg.Text('千焦(KJ)', font=('微软雅黑', 12))],
        [sg.Text('克(g)', font=('微软雅黑', 12))],
        [sg.Text('克(g)', font=('微软雅黑', 12))],
        [sg.Text('克(g)', font=('微软雅黑', 12))],
        [sg.Text('毫克(mg)', font=('微软雅黑', 12))],
    ]
    layout = [
        [sg.Frame(layout=rc_11, title='项目', font=('微软雅黑', 12)),
         sg.Frame(layout=rc_12, title='原始数值', font=('微软雅黑', 12)),
         sg.Frame(layout=rc_13, title='修约数值', font=('微软雅黑', 12)),
         sg.Frame(layout=rc_14, title='NRV%(原始)', font=('微软雅黑', 12)),
         sg.Frame(layout=rc_15, title='NRV%(修约)', font=('微软雅黑', 12)),
         sg.Frame(layout=rc_16, title='单位', font=('微软雅黑', 12))],
        [sg.Button('从剪贴板导入', key='导入', font=('微软雅黑', 12)),
         sg.Button('计算', key='计算', font=('微软雅黑', 12)),
         sg.Button('清空', key='清空', font=('微软雅黑', 12))],
        [sg.StatusBar('准备就绪', text_color="black", justification='center', key='status', font=('微软雅黑', 12),
                      size=(10, 1))],
    ]
    return sg.Window(
        '营养成分表修约(基础)',
        layout,
        enable_close_attempted_event=True,
        element_justification='center',
        finalize=True,
        return_keyboard_events=True)


def nutrition(window):
    window.Hide()
    window_item = nutrition_win()
    while True:
        event_n, values_n = window_item.read()
        if event_n == '-WINDOW CLOSE ATTEMPTED-':
            window_item.close()
            window.UnHide()
            return window
        elif event_n in ['计算', '\r']:
            try:
                del values_n['status']
                numbers = [decimal.Decimal(i) for i in values_n.values()]
                # window_item.find_element('status').update('准备就绪', text_color="black")
            except decimal.InvalidOperation:
                window_item.find_element('status').update(
                    '输入数值无效！', text_color="black")
                continue
            limit = [decimal.Decimal(i)
                     for i in ('17', '0.5', '0.5', '0.5', '5')]
            standard = [
                decimal.Decimal(i) for i in (
                    '8400', '60', '60', '300', '2000')]
            energy = []
            for i, j in zip((0, 1, 2, 3, 4), ('1.', '.0', '.0', '.0', '1.')):
                if numbers[i] > limit[i]:
                    num = numbers[i].quantize(
                        decimal.Decimal(j), rounding=decimal.ROUND_HALF_EVEN)
                    if 1 <= i <= 3:
                        energy.append(num)
                    window_item.find_element('1' + str(i)).update(num)
                    nrv = (
                            (num /
                             standard[i]) *
                            decimal.Decimal('100')).quantize(
                        decimal.Decimal('.0000'),
                        rounding=decimal.ROUND_HALF_EVEN)
                    window_item.find_element(
                        '2' +
                        str(i)).update(
                        '%.2f%%' %
                        nrv)
                    if decimal.Decimal('0.5') <= nrv <= decimal.Decimal('1'):
                        window_item.find_element('3' + str(i)).update('1%')
                    else:
                        window_item.find_element(
                            '3' +
                            str(i)).update(
                            '%.0f%%' %
                            ((num /
                              standard[i]) *
                             decimal.Decimal('100')).quantize(
                                decimal.Decimal('.00'),
                                rounding=decimal.ROUND_HALF_EVEN))
                else:
                    if 1 <= i <= 3:
                        energy.append(decimal.Decimal('0'))
                    window_item.find_element('1' + str(i)).update('0')
                    window_item.find_element('2' + str(i)).update('0%')
                    window_item.find_element('3' + str(i)).update('0%')
            energy = (energy[0] * decimal.Decimal('17')) + (energy[1] *
                                                            decimal.Decimal('37')) + (energy[2] * decimal.Decimal('17'))
            energy_round = energy.quantize(
                decimal.Decimal('1.'),
                rounding=decimal.ROUND_HALF_EVEN)
            energy_nrv = (
                    energy_round *
                    decimal.Decimal('100') /
                    decimal.Decimal('8400')).quantize(
                decimal.Decimal('.0000'),
                rounding=decimal.ROUND_HALF_EVEN)
            correct = bool(abs(energy - numbers[0]) <= decimal.Decimal('20.0'))
            window_item.find_element('status').update(
                '能量计算结果分别为：%s，%s，%.2f%%，%.0f%%' %
                (energy, energy_round, energy_nrv, energy_nrv.quantize(
                    decimal.Decimal('.00'), rounding=decimal.ROUND_HALF_EVEN)),
                text_color={True: "green", False: "red"}[correct])
        elif event_n == '导入':
            data = pyperclip.paste()
            data = data.split('\r\n')
            if len(data) == 6:
                data = data[:-1]  # 可优化
            if len(data) == 5:
                for i, j, l in zip(
                        (0, 1, 2, 3, 4), data, (-6, -4, -4, -4, -6)):
                    window_item.find_element('0' + str(i)).update(j[:l])
                window_item.find_element('status').update(
                    '导入成功！', text_color="black")
            else:
                window_item.find_element('status').update(
                    '导入失败，请检查复制内容！', text_color="black")
        elif event_n == '清空':
            for i in range(5):
                window_item.find_element('0' + str(i)).update('')
            window_item.find_element('status').update(
                '准备就绪', text_color="black")


def nutrition_plus_win():
    rc_11 = [
        [sg.Text('能量', font=('微软雅黑', 12))],
        [sg.Text('蛋白质', font=('微软雅黑', 12))],
        [sg.Text('脂肪', font=('微软雅黑', 12))],
        [sg.Text('碳水化合物', font=('微软雅黑', 12))],
        [sg.Text('钠', font=('微软雅黑', 12))],
        [sg.Text('膳食纤维', font=('微软雅黑', 12))],
        [sg.Text('维生素E', font=('微软雅黑', 12))],
        [sg.Text('维生素B1', font=('微软雅黑', 12))],
        [sg.Text('维生素B2', font=('微软雅黑', 12))],
        [sg.Text('维生素C', font=('微软雅黑', 12))],
        [sg.Text('叶酸', font=('微软雅黑', 12))],
        [sg.Text('钾', font=('微软雅黑', 12))],
        [sg.Text('钙', font=('微软雅黑', 12))],
        [sg.Text('铁', font=('微软雅黑', 12))],
        [sg.Text('锌', font=('微软雅黑', 12))],
        [sg.Text('硒', font=('微软雅黑', 12))],
    ]
    rc_12 = [
        [sg.Input(key='000', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Input(key='001', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Input(key='002', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Input(key='003', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Input(key='004', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Input(key='005', size=(10, 1), font=('微软雅黑', 12), default_text='0')],
        [sg.Input(key='006', size=(10, 1), font=('微软雅黑', 12), default_text='0')],
        [sg.Input(key='007', size=(10, 1), font=('微软雅黑', 12), default_text='0')],
        [sg.Input(key='008', size=(10, 1), font=('微软雅黑', 12), default_text='0')],
        [sg.Input(key='009', size=(10, 1), font=('微软雅黑', 12), default_text='0')],
        [sg.Input(key='010', size=(10, 1), font=('微软雅黑', 12), default_text='0')],
        [sg.Input(key='011', size=(10, 1), font=('微软雅黑', 12), default_text='0')],
        [sg.Input(key='012', size=(10, 1), font=('微软雅黑', 12), default_text='0')],
        [sg.Input(key='013', size=(10, 1), font=('微软雅黑', 12), default_text='0')],
        [sg.Input(key='014', size=(10, 1), font=('微软雅黑', 12), default_text='0')],
        [sg.Input(key='015', size=(10, 1), font=('微软雅黑', 12), default_text='0')],
    ]
    rc_13 = [
        [sg.Text(key='100', size=(5, 1), font=('微软雅黑', 12))],
        [sg.Text(key='101', size=(5, 1), font=('微软雅黑', 12))],
        [sg.Text(key='102', size=(5, 1), font=('微软雅黑', 12))],
        [sg.Text(key='103', size=(5, 1), font=('微软雅黑', 12))],
        [sg.Text(key='104', size=(5, 1), font=('微软雅黑', 12))],
        [sg.Text(key='105', size=(5, 1), font=('微软雅黑', 12))],
        [sg.Text(key='106', size=(5, 1), font=('微软雅黑', 12))],
        [sg.Text(key='107', size=(5, 1), font=('微软雅黑', 12))],
        [sg.Text(key='108', size=(5, 1), font=('微软雅黑', 12))],
        [sg.Text(key='109', size=(5, 1), font=('微软雅黑', 12))],
        [sg.Text(key='110', size=(5, 1), font=('微软雅黑', 12))],
        [sg.Text(key='111', size=(5, 1), font=('微软雅黑', 12))],
        [sg.Text(key='112', size=(5, 1), font=('微软雅黑', 12))],
        [sg.Text(key='113', size=(5, 1), font=('微软雅黑', 12))],
        [sg.Text(key='114', size=(5, 1), font=('微软雅黑', 12))],
        [sg.Text(key='115', size=(5, 1), font=('微软雅黑', 12))],
    ]
    rc_14 = [
        [sg.Text(key='200', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='201', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='202', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='203', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='204', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='205', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='206', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='207', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='208', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='209', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='210', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='211', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='212', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='213', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='214', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='215', size=(10, 1), font=('微软雅黑', 12))],
    ]
    rc_15 = [
        [sg.Text(key='300', size=(5, 1), font=('微软雅黑', 12))],
        [sg.Text(key='301', size=(5, 1), font=('微软雅黑', 12))],
        [sg.Text(key='302', size=(5, 1), font=('微软雅黑', 12))],
        [sg.Text(key='303', size=(5, 1), font=('微软雅黑', 12))],
        [sg.Text(key='304', size=(5, 1), font=('微软雅黑', 12))],
        [sg.Text(key='305', size=(5, 1), font=('微软雅黑', 12))],
        [sg.Text(key='306', size=(5, 1), font=('微软雅黑', 12))],
        [sg.Text(key='307', size=(5, 1), font=('微软雅黑', 12))],
        [sg.Text(key='308', size=(5, 1), font=('微软雅黑', 12))],
        [sg.Text(key='309', size=(5, 1), font=('微软雅黑', 12))],
        [sg.Text(key='310', size=(5, 1), font=('微软雅黑', 12))],
        [sg.Text(key='311', size=(5, 1), font=('微软雅黑', 12))],
        [sg.Text(key='312', size=(5, 1), font=('微软雅黑', 12))],
        [sg.Text(key='313', size=(5, 1), font=('微软雅黑', 12))],
        [sg.Text(key='314', size=(5, 1), font=('微软雅黑', 12))],
        [sg.Text(key='315', size=(5, 1), font=('微软雅黑', 12))],
    ]
    rc_16 = [
        [sg.Text('千焦(KJ)', font=('微软雅黑', 12))],
        [sg.Text('克(g)', font=('微软雅黑', 12))],
        [sg.Text('克(g)', font=('微软雅黑', 12))],
        [sg.Text('克(g)', font=('微软雅黑', 12))],
        [sg.Text('毫克(mg)', font=('微软雅黑', 12))],
        [sg.Text('克(g)', font=('微软雅黑', 12))],
        [sg.Text('mg α-TE', font=('微软雅黑', 12))],
        [sg.Text('毫克(mg)', font=('微软雅黑', 12))],
        [sg.Text('毫克(mg)', font=('微软雅黑', 12))],
        [sg.Text('毫克(mg)', font=('微软雅黑', 12))],
        [sg.Text('ugDFE', font=('微软雅黑', 12))],
        [sg.Text('毫克(mg)', font=('微软雅黑', 12))],
        [sg.Text('毫克(mg)', font=('微软雅黑', 12))],
        [sg.Text('毫克(mg)', font=('微软雅黑', 12))],
        [sg.Text('毫克(mg)', font=('微软雅黑', 12))],
        [sg.Text('微克(μg)', font=('微软雅黑', 12))],
    ]
    layout = [
        [sg.Frame(layout=rc_11, title='项目', font=('微软雅黑', 12)),
         sg.Frame(layout=rc_12, title='原始数值', font=('微软雅黑', 12)),
         sg.Frame(layout=rc_13, title='修约数值', font=('微软雅黑', 12)),
         sg.Frame(layout=rc_14, title='NRV%(原始)', font=('微软雅黑', 12)),
         sg.Frame(layout=rc_15, title='NRV%(修约)', font=('微软雅黑', 12)),
         sg.Frame(layout=rc_16, title='单位', font=('微软雅黑', 12))],
        [sg.Button('从剪贴板导入', key='导入', font=('微软雅黑', 12)),
         sg.Button('计算', key='计算', font=('微软雅黑', 12)), sg.Button('清空', key='清空', font=('微软雅黑', 12))],
        [sg.StatusBar('准备就绪', text_color="black", justification='center', key='status', font=('微软雅黑', 12),
                      size=(10, 1))],
    ]
    return sg.Window(
        '营养成分表修约(详细)',
        layout,
        enable_close_attempted_event=True,
        element_justification='center',
        finalize=True,
        return_keyboard_events=True)


def nutrition_plus(window):
    window.Hide()
    window_item = nutrition_plus_win()
    while True:
        event_np, values_np = window_item.read()
        if event_np == '-WINDOW CLOSE ATTEMPTED-':
            window_item.close()
            window.UnHide()
            return window
        elif event_np in ['计算', '\r']:
            try:
                del values_np['status']
                numbers = [decimal.Decimal(i) for i in values_np.values()]
                # window_item.find_element('status').update('准备就绪', text_color="black")
            except decimal.InvalidOperation:
                window_item.find_element('status').update(
                    '输入数值无效！', text_color="black")
                continue
            limit = [
                decimal.Decimal(i) for i in (
                    '17',
                    '0.5',
                    '0.5',
                    '0.5',
                    '5',
                    '0.5',
                    '0.28',
                    '0.03',
                    '0.03',
                    '2.0',
                    '8',
                    '20',
                    '8',
                    '0.3',
                    '0.30',
                    '1.0')]
            standard = [
                decimal.Decimal(i) for i in (
                    '8400',
                    '60',
                    '60',
                    '300',
                    '2000',
                    '25',
                    '14',
                    '1.4',
                    '1.4',
                    '100',
                    '400',
                    '2000',
                    '800',
                    '15',
                    '15',
                    '50')]
            energy = []
            for i, j in zip((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15), ('1.', '.0', '.0',
                                                                                     '.0', '1.', '.0', '.00', '.00',
                                                                                     '.00', '.0', '1.', '1.', '1.',
                                                                                     '.0', '.00', '.0')):
                if numbers[i] > limit[i]:
                    num = numbers[i].quantize(
                        decimal.Decimal(j), rounding=decimal.ROUND_HALF_EVEN)
                    if i in (1, 2, 3, 5):
                        energy.append(num)
                    window_item.find_element('1' + str(i).zfill(2)).update(num)
                    nrv = ((num / standard[i]) *
                           decimal.Decimal('100')).quantize(
                        decimal.Decimal('.0000'),
                        rounding=decimal.ROUND_HALF_EVEN)
                    window_item.find_element(
                        '2' +
                        str(i).zfill(2)).update(
                        '%.2f%%' %
                        nrv)
                    if decimal.Decimal('0.5') <= nrv <= decimal.Decimal('1'):
                        window_item.find_element(
                            '3' + str(i).zfill(2)).update('1%')
                    else:
                        window_item.find_element(
                            '3' +
                            str(i).zfill(2)).update(
                            '%.0f%%' %
                            ((num /
                              standard[i]) *
                             decimal.Decimal('100')).quantize(
                                decimal.Decimal('.00'),
                                rounding=decimal.ROUND_HALF_EVEN))
                else:
                    if i in (1, 2, 3, 5):
                        energy.append(decimal.Decimal('0'))
                    window_item.find_element('1' + str(i).zfill(2)).update('0')
                    window_item.find_element(
                        '2' + str(i).zfill(2)).update('0%')
                    window_item.find_element(
                        '3' + str(i).zfill(2)).update('0%')
            energy = (energy[0] * decimal.Decimal('17')) + (energy[1] *
                                                            decimal.Decimal('37')) + (energy[2] * decimal.Decimal('17'))
            energy_round = energy.quantize(
                decimal.Decimal('1.'),
                rounding=decimal.ROUND_HALF_EVEN)
            energy_nrv = (
                    energy_round *
                    decimal.Decimal('100') /
                    decimal.Decimal('8400')).quantize(
                decimal.Decimal('.0000'),
                rounding=decimal.ROUND_HALF_EVEN)
            correct = bool(abs(energy - numbers[0]) <= decimal.Decimal('20.0'))
            window_item.find_element('status').update(
                '能量计算结果分别为：%s，%s，%.2f%%，%.0f%%' %
                (energy, energy_round, energy_nrv, energy_nrv.quantize(
                    decimal.Decimal('.00'), rounding=decimal.ROUND_HALF_EVEN)),
                text_color={True: "green", False: "red"}[correct])
        elif event_np == '导入':
            data = pyperclip.paste()
            data = data.split('\r\n')
            if len(data) == 6:
                data = data[:-1]  # 可优化
            if len(data) == 5:
                for i, j, l in zip(
                        (0, 1, 2, 3, 4), data, (-6, -4, -4, -4, -6)):
                    window_item.find_element('00' + str(i)).update(j[:l])
                window_item.find_element('status').update(
                    '导入成功！', text_color="black")
            else:
                window_item.find_element('status').update(
                    '导入失败，请检查复制内容！', text_color="black")
        elif event_np == '清空':
            for i in range(5):
                window_item.find_element('0' + str(i).zfill(2)).update('')
            for i in range(5, 16):
                window_item.find_element('0' + str(i).zfill(2)).update('0')
            window_item.find_element('status').update(
                '准备就绪', text_color="black")


def dehydration_win():
    rc_11 = [
        [sg.Text('鲜品水分', font=('微软雅黑', 12))],
        [sg.Text('本品水分', font=('微软雅黑', 12))],
        [sg.Text('铅(mg/kg)', font=('微软雅黑', 12))],
        [sg.Text('总砷(mg/kg)', font=('微软雅黑', 12))],
        [sg.Text('镉(mg/kg)', font=('微软雅黑', 12))],
        [sg.Text('总汞(mg/kg)', font=('微软雅黑', 12))],
        [sg.Text('铬(mg/kg)', font=('微软雅黑', 12))],
        [sg.Text('其他限值一', font=('微软雅黑', 12))],
        [sg.Text('其他限值二', font=('微软雅黑', 12))],
        [sg.Text('其他限值三', font=('微软雅黑', 12))],
    ]
    rc_12 = [
        [sg.Input(key='00', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Input(key='01', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Input(key='02', size=(10, 1), default_text='0', font=('微软雅黑', 12))],
        [sg.Input(key='03', size=(10, 1), default_text='0', font=('微软雅黑', 12))],
        [sg.Input(key='04', size=(10, 1), default_text='0', font=('微软雅黑', 12))],
        [sg.Input(key='05', size=(10, 1), default_text='0', font=('微软雅黑', 12))],
        [sg.Input(key='06', size=(10, 1), default_text='0', font=('微软雅黑', 12))],
        [sg.Input(key='07', size=(10, 1), default_text='0', font=('微软雅黑', 12))],
        [sg.Input(key='08', size=(10, 1), default_text='0', font=('微软雅黑', 12))],
        [sg.Input(key='09', size=(10, 1), default_text='0', font=('微软雅黑', 12))],
    ]
    rc_13 = [
        [sg.Text(key='10', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='11', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='12', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='13', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='14', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='15', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='16', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='17', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='18', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='19', size=(10, 1), font=('微软雅黑', 12))],
    ]
    rc_14 = [
        [sg.Text(size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='22', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='23', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='24', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='25', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='26', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='27', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='28', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='29', size=(10, 1), font=('微软雅黑', 12))],
    ]
    rc_21 = [
        [sg.Button('香菇', key='香菇', font=('微软雅黑', 10)), sg.Button('鲜枣', key='鲜枣', font=('微软雅黑', 10)),
         sg.Button('葡萄', key='葡萄', font=('微软雅黑', 10)), sg.Button('木耳/银耳', key='木耳', font=('微软雅黑', 10)),
         sg.Button('大白菜', key='大白菜', font=('微软雅黑', 10)), sg.Button('黄花菜', key='黄花菜', font=('微软雅黑', 10)),
         sg.Button('芥菜', key='芥菜', font=('微软雅黑', 10)), sg.Button('青鳞鱼', key='青鳞鱼', font=('微软雅黑', 10))],
        [sg.Button('鲢鱼', key='鲢鱼', font=('微软雅黑', 10)), sg.Button('豆角', key='豆角', font=('微软雅黑', 10)),
         sg.Button('鱿鱼', key='鱿鱼', font=('微软雅黑', 10)), sg.Button('柠檬', key='柠檬', font=('微软雅黑', 10)),
         sg.Button('柚', key='柚', font=('微软雅黑', 10)), sg.Button('西柚', key='西柚', font=('微软雅黑', 10)),
         sg.Button('猪肉', key='猪肉', font=('微软雅黑', 10)), sg.Button('食用菌(除香菇外)', key='食用菌', font=('微软雅黑', 10))],
    ]
    layout = [
        [sg.Frame(layout=rc_11, title='项目', font=('微软雅黑', 12)),
         sg.Frame(layout=rc_12, title='数值', font=('微软雅黑', 12)),
         sg.Frame(layout=rc_13, title='结果(原始)', font=('微软雅黑', 12)),
         sg.Frame(layout=rc_14, title='结果(修约)', font=('微软雅黑', 12))],
        [sg.StatusBar('准备就绪', justification='center', key='status', font=('微软雅黑', 12), size=(10, 1))],
        [sg.Button('计算', key='计算', font=('微软雅黑', 12)), sg.Button('清空', key='清空', font=('微软雅黑', 12)),
         sg.Button('复制备注', key='备注', font=('微软雅黑', 12))],
        [sg.Frame(layout=rc_21, title='常见样品', font=('微软雅黑', 12))]
    ]
    return sg.Window(
        '脱水率及限值计算',
        layout,
        enable_close_attempted_event=True,
        element_justification='center',
        finalize=True,
        return_keyboard_events=True)


def dehydration(window):
    window.Hide()
    window_item = dehydration_win()
    remark = None
    while True:
        event_d, values_d = window_item.read()
        if event_d == '-WINDOW CLOSE ATTEMPTED-':
            window_item.close()
            window.UnHide()
            return window
        elif event_d in ['计算', '\r']:
            try:
                del values_d['status']
                numbers = [decimal.Decimal(i) for i in values_d.values()]
            except decimal.InvalidOperation:
                window_item.find_element('status').update('输入数值无效！')
                continue
            fresh = decimal.Decimal(numbers[0])
            real = decimal.Decimal(numbers[1])
            if fresh < real or real == decimal.Decimal('100'):
                window_item.find_element('status').update('输入数值无效！')
                continue
            if fresh == decimal.Decimal('100'):
                result = real / decimal.Decimal('100')
            else:
                result = ((fresh - real) / (decimal.Decimal('100') - real))
            window_item.find_element('status').update(
                '脱水率：%.1f%%' %
                (result *
                 decimal.Decimal('100')).quantize(
                    decimal.Decimal('.000'),
                    rounding=decimal.ROUND_HALF_EVEN))
            window_item.find_element('10').update(
                '%.1f%%' %
                fresh.quantize(
                    decimal.Decimal('.0'),
                    rounding=decimal.ROUND_HALF_EVEN))
            window_item.find_element('11').update(
                '%.1f%%' %
                real.quantize(
                    decimal.Decimal('.000'),
                    rounding=decimal.ROUND_HALF_EVEN))
            remark = []
            for i, j in zip((2, 3, 4, 5, 6, 7, 8, 9), numbers[2:]):
                if numbers[i] > decimal.Decimal('0'):
                    length = valid_numbers(str(numbers[i])) + '0'
                    window_item.find_element(
                        '1' + str(i)).update((numbers[i] / (1 - result)).quantize(decimal.Decimal('.000000'),
                                                                                  rounding=decimal.ROUND_HALF_EVEN))
                    cache = (
                            numbers[i] /
                            (
                                    1 -
                                    result)).quantize(
                        decimal.Decimal(length),
                        rounding=decimal.ROUND_HALF_EVEN)
                    window_item.find_element('2' + str(i)).update(cache)
                    if 2 <= i <= 6:
                        remark.append((DEHYDRATION_ITEMS[i], cache))
                else:
                    window_item.find_element('1' + str(i)).update('0')
                    window_item.find_element('2' + str(i)).update('0')
        elif event_d == '清空':
            for i in range(10):
                window_item.find_element('0' + str(i)).update('0')
            window_item.find_element('status').update('准备就绪')
            remark = None
        elif event_d == '备注':
            if not remark:
                window_item.find_element('status').update('复制备注失败！')
                continue
            del values_d['status']
            numbers = [decimal.Decimal(i) for i in values_d.values()]
            fresh = decimal.Decimal(numbers[0])
            real = decimal.Decimal(numbers[1])
            items = '，'.join('%s限量为%smg/kg' % i for i in remark)
            if fresh == decimal.Decimal('100'):
                result = real / decimal.Decimal('100')
                text = '根据委托单位提供该产品的脱水率为%.1f%%。以此为依据，折算该样品%s。' % ((result * decimal.Decimal(
                    '100')).quantize(decimal.Decimal('.000'), rounding=decimal.ROUND_HALF_EVEN), items)
            else:
                result = (fresh - real) / (decimal.Decimal('100') - real)
                text = '根据《中国食物成分表》中XXX水分含量%.1f%%，本品水分含量为%.1f%%，经过计算得出该产品的脱水率为%.1f%%。' \
                       '以此为依据，折算该样品%s。' % \
                       (fresh, real, (result * 100).quantize(decimal.Decimal('.000'), rounding=decimal.ROUND_HALF_EVEN),
                        items)
            pyperclip.copy(text)
            window_item.find_element('status').update(
                '脱水率：%.1f%%，复制备注成功！' %
                (result *
                 decimal.Decimal('100')).quantize(
                    decimal.Decimal('.000'),
                    rounding=decimal.ROUND_HALF_EVEN))
        elif event_d in LIMIT.keys():
            for i in range(7):
                window_item.find_element(
                    '0' +
                    str(i)).update(
                    LIMIT[event_d][i])
            window_item.find_element('status').update('准备就绪')
            remark = None


def clipboard_win():
    rc_11 = [
        [sg.Button('微生物🔺备注', key='00', font=('微软雅黑', 10))],
        [sg.Button('监督抽检不判定结论', key='14', font=('微软雅黑', 10))],
        [sg.Button('作废报告备注', key='15', font=('微软雅黑', 10))],
        [sg.Button('标签审核结论', key='20', font=('微软雅黑', 10))],
        [sg.Button('酒精度限值', key='01', font=('微软雅黑', 10))],
        [sg.Button('阳性验证结论', key='16', font=('微软雅黑', 10))],
        [sg.Button('甲基汞备注', key='18', font=('微软雅黑', 10))],
        [sg.Button('多氯联苯备注', key='17', font=('微软雅黑', 10))],
    ]
    rc_12 = [
        [sg.Button('761 666检测限', key='02', font=('微软雅黑', 10))],
        [sg.Button('761 DDT检测限', key='03', font=('微软雅黑', 10))],
        [sg.Button('5009.19 666植物油检测限', key='04', font=('微软雅黑', 10))],
        [sg.Button('5009.19 DDT植物油检测限', key='05', font=('微软雅黑', 10))],
        [sg.Button('23200.13 666茶叶定量限', key='19', font=('微软雅黑', 10))],
    ]
    rc_13 = [
        [sg.Button('格式标签-预包装', key='06', font=('微软雅黑', 10))],
        [sg.Button('格式标签-非预包装', key='07', font=('微软雅黑', 10))],
        [sg.Button('详细标签-实物', key='08', font=('微软雅黑', 10))],
        [sg.Button('详细标签-电子版', key='09', font=('微软雅黑', 10))],
        [sg.Button('详细标签-无许可证电子版', key='10', font=('微软雅黑', 10))],
        [sg.Button('详细标签-非预包装电子版', key='11', font=('微软雅黑', 10))],
        [sg.Button('详细标签-非预包装实物版', key='12', font=('微软雅黑', 10))],
        [sg.Button('详细标签-样版标签', key='13', font=('微软雅黑', 10))],
    ]
    layout = [
        [sg.Frame(layout=rc_11, title='未分类', font=('微软雅黑', 12)),
         sg.Frame(layout=rc_12, title='检测限', font=('微软雅黑', 12)),
         sg.Frame(layout=rc_13, title='标签备注', font=('微软雅黑', 12))],
    ]
    return sg.Window(
        '常用文本剪贴板（点击按钮复制相应文本）',
        layout,
        enable_close_attempted_event=True,
        element_justification='center',
        finalize=True)


def clipboard(window):
    window.Hide()
    window_item = clipboard_win()
    while True:
        event_d, values_d = window_item.read()
        if event_d == '-WINDOW CLOSE ATTEMPTED-':
            window_item.close()
            window.UnHide()
            return window
        elif event_d in [str(i).zfill(2) for i in range(21)]:
            pyperclip.copy(TEXT[event_d])


def solid_drink_win():
    rc_11 = [
        [sg.Text('样品量(g)', font=('微软雅黑', 12))],
        [sg.Text('水(ml)', font=('微软雅黑', 12))],
        [sg.Text('苯甲酸', font=('微软雅黑', 12))],
        [sg.Text('山梨酸', font=('微软雅黑', 12))],
        [sg.Text('苋菜红', font=('微软雅黑', 12))],
        [sg.Text('柠檬黄', font=('微软雅黑', 12))],
        [sg.Text('胭脂红', font=('微软雅黑', 12))],
        [sg.Text('其他限值一', font=('微软雅黑', 12))],
        [sg.Text('其他限值二', font=('微软雅黑', 12))],
        [sg.Text('其他限值三', font=('微软雅黑', 12))],
    ]
    rc_12 = [
        [sg.Input(key='00', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Input(key='01', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Input('0', key='02', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Input('0', key='03', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Input('0', key='04', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Input('0', key='05', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Input('0', key='06', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Input('0', key='07', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Input('0', key='08', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Input('0', key='09', size=(10, 1), font=('微软雅黑', 12))],
    ]
    rc_13 = [
        [sg.Text(size=(5, 1), font=('微软雅黑', 12))],
        [sg.Text(size=(5, 1), font=('微软雅黑', 12))],
        [sg.Text(key='12', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='13', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='14', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='15', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='16', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='17', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='18', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='19', size=(10, 1), font=('微软雅黑', 12))],
    ]
    rc_21 = [
        [sg.Button('饮料大类', key='饮料', font=('微软雅黑', 10)),
         sg.Button('果蔬汁类饮料', key='果蔬汁', font=('微软雅黑', 10)),
         sg.Button('植物蛋白饮料', key='植物蛋白', font=('微软雅黑', 10))],
        [sg.Button('含乳饮料', key='含乳', font=('微软雅黑', 10)),
         sg.Button('碳酸饮料', key='碳酸', font=('微软雅黑', 10)),
         sg.Button('风味饮料', key='风味', font=('微软雅黑', 10)),
         sg.Button('果味饮料', key='果味', font=('微软雅黑', 10))],
    ]
    layout = [
        [sg.Frame(layout=rc_11, title='项目', font=('微软雅黑', 12)),
         sg.Frame(layout=rc_12, title='原始数值', font=('微软雅黑', 12)),
         sg.Frame(layout=rc_13, title='结果数值', font=('微软雅黑', 12))],
        [sg.Button('计算', key='计算', font=('微软雅黑', 12)),
         sg.Button('清空', key='清空', font=('微软雅黑', 12)),
         sg.Button('复制备注', key='备注', font=('微软雅黑', 12))],
        [sg.StatusBar('准备就绪', justification='center',
                      key='status', font=('微软雅黑', 12), size=(10, 1))],
        [sg.Frame(layout=rc_21, title='常见固体饮料', font=('微软雅黑', 12))],
    ]
    return sg.Window(
        '固体饮料限值计算',
        layout,
        enable_close_attempted_event=True,
        element_justification='center',
        finalize=True,
        return_keyboard_events=True)


def solid_drink(window):
    window.Hide()
    window_item = solid_drink_win()
    remark = None
    while True:
        event_s, values_s = window_item.read()
        if event_s == '-WINDOW CLOSE ATTEMPTED-':
            window_item.close()
            window.UnHide()
            return window
        elif event_s in ['计算', '\r']:
            try:
                del values_s['status']
                numbers = [decimal.Decimal(i) for i in values_s.values()]
                window_item.find_element('status').update('准备就绪')
            except decimal.InvalidOperation:
                window_item.find_element('status').update('输入数值无效！')
                continue
            if decimal.Decimal('0') in numbers[:2]:
                window_item.find_element('status').update('输入数值无效！')
                continue
            multiple = (numbers[0] + numbers[1]) / numbers[0]
            length_m = valid_numbers(str(multiple), min_=True)
            window_item.find_element('status').update(
                '倍数：%s' %
                multiple.quantize(
                    decimal.Decimal(length_m),
                    rounding=decimal.ROUND_HALF_EVEN))
            remark = []
            for i, j in zip((2, 3, 4, 5, 6, 7, 8, 9), numbers[2:]):
                if numbers[i] > decimal.Decimal('0'):
                    result = numbers[i] * multiple
                    length_r = valid_numbers(str(result), min_=True)
                    result = result.quantize(
                        decimal.Decimal(length_r),
                        rounding=decimal.ROUND_HALF_EVEN)
                    window_item.find_element('1' + str(i)).update(result)
                    if 2 <= i <= 6:
                        remark.append(SOLID_ITEMS[i])
                else:
                    window_item.find_element('1' + str(i)).update('0')
        elif event_s == '备注':
            if not remark:
                window_item.find_element('status').update('复制备注失败！')
                continue
            del values_s['status']
            numbers = [decimal.Decimal(i) for i in values_s.values()]
            multiple = (numbers[0] + numbers[1]) / numbers[0]
            length_m = valid_numbers(str(multiple), min_=True)
            text = '样品冲调比例：将每包（%sg）XXX固体饮料加%s毫升清水冲调。项目“%s”按稀释倍数折算。' % (
                numbers[0], numbers[1], '、'.join(remark))
            pyperclip.copy(text)
            window_item.find_element('status').update(
                '倍数：%s，复制备注成功！' %
                multiple.quantize(
                    decimal.Decimal(length_m),
                    rounding=decimal.ROUND_HALF_EVEN))
        elif event_s == '清空':
            for i in range(10):
                window_item.find_element('0' + str(i)).update('0')
            window_item.find_element('status').update('准备就绪')
            remark = None
        elif event_s in SOLID.keys():
            for i, j in zip((2, 3, 4, 5, 6), (0, 1, 2, 3, 4)):
                window_item.find_element(
                    '0' +
                    str(i)).update(
                    SOLID[event_s][j])
            window_item.find_element('status').update('准备就绪')
            remark = None


def main():
    sg.theme('GreenMono')
    window = home()
    while True:
        event, values = window.read()
        if event is None:
            break
        elif event == '营养成分表(基础)':
            window = nutrition(window)
        elif event == '营养成分表(详细)':
            window = nutrition_plus(window)
        elif event == '脱水率及限值计算':
            window = dehydration(window)
        elif event == '常用文本剪贴板':
            window = clipboard(window)
        elif event == '固体饮料限值计算':
            window = solid_drink(window)
        elif event == '查看工具详细说明':
            webbrowser.open(
                'https://github.com/JoeanAmiee/Private_office_tools')


if __name__ == '__main__':
    main()
