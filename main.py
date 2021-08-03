import decimal
import PySimpleGUI as sg
import pyperclip

TEXT = {
    '00': '△：n：同一批次产品应采集的样品件数，c：最大可允许超出m值的样品件数，m：微生物指标可接受水平的限量值，M：微生物指标的最高安全限值。',
    '01': '酒精度实测值与标签标示值允许差为±1.0%vol（标签标示值：43%vol）',
    '02': 'α-666：0.0001\nβ-666：0.0004\nγ-666：0.0002\nδ-666：0.0001',
    '03': 'p,p’-DDE：0.0001\no,p’-DDE：0.0002\no,p’-DDD：0.0004\np,p’-DDT：0.0009',
    '04': 'α-六六六：\n0.000097\nβ-六六六：\n0.000634\nγ-六六六：\n0.000226\nδ-六六六：\n0.000179',
    '05': 'P,P’-滴滴伊：\n0.000345\nO,P’-滴滴涕：\n0.000412\nP,P’-滴滴滴：\n0.000465\nP,P’-滴滴涕：\n0.000481',
    '06': '标签审核内容不包括标示内容真实性和规范性的核实。',
    '07': '标签审核内容不包括标示内容真实性和规范性的核实。\n该样品为散装称重食品，参照GB 7718-2011、GB 28050-2011的要求进行审核，审核内容不包括净含量和规格。',
    '08': '标签审核内容不包括标示内容真实性的核实。',
    '09': '样品为电子标签，标签审核内容不包括强制标示内容的字符高度以及生产日期格式，以实物印刷为准。\n标签审核内容不包括标示内容真实性的核实。',
    '10': '样品为电子标签，标签审核内容不包括强制标示内容的字符高度以及生产日期格式，以实物印刷为准。\n标签审核内容不包括标示内容真实性的核实。\n本报告用于发证检验，食品生产许可证编号不在本次标签审核范围内。',
    '11': '样品为电子标签，标签审核内容不包括强制标示内容的字符高度以及生产日期格式，以实物印刷为准。\n标签审核内容不包括标示内容真实性的核实。\n该样品为散装称重食品，参照GB 7718-2011、GB 28050-2011的要求进行审核，审核内容不包括净含量和规格。',
    '12': '标签审核内容不包括标示内容真实性的核实。\n该样品为散装称重食品，参照GB 7718-2011、GB 28050-2011的要求进行审核，审核内容不包括净含量和规格。',
    '13': '样品为样版标签，标签审核内容不包括生产日期字符高度及格式，以实物印刷为准。\n标签审核内容不包括标示内容真实性的核实。',
}


def valid_numbers(numbers):
    if numbers[0] != '0':
        return 1
    numbers = numbers.lstrip('0')
    numbers = numbers.rstrip('0')
    return len(numbers) - 1


def home():
    layout = [
        [sg.Button('营养成分表(基础)', size=(16, 2), font=('微软雅黑', 12))],
        [sg.Button('营养成分表(详细)', size=(16, 2), font=('微软雅黑', 12))],
        [sg.Button('脱水率计算', size=(16, 2), font=('微软雅黑', 12))],
        [sg.Button('常用剪贴板', size=(16, 2), font=('微软雅黑', 12))],
    ]
    return sg.Window(
        '小工具 beta',
        layout,
        size=(
            260,
            300),
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
        [sg.Input(key='00', size=(10, 0), font=('微软雅黑', 12))],
        [sg.Input(key='01', size=(10, 0), font=('微软雅黑', 12))],
        [sg.Input(key='02', size=(10, 0), font=('微软雅黑', 12))],
        [sg.Input(key='03', size=(10, 0), font=('微软雅黑', 12))],
        [sg.Input(key='04', size=(10, 0), font=('微软雅黑', 12))],
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
        [sg.Button('计算', key='计算', font=('微软雅黑', 12)), sg.Button('清空', key='清空', font=('微软雅黑', 12))],
        [sg.StatusBar('运行正常', justification='center', key='status', font=('微软雅黑', 12), size=(10, 1))],
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
            window.un_hide()
            return window
        elif event_n in ['计算', '\r']:
            try:
                del values_n['status']
                numbers = [decimal.Decimal(i) for i in values_n.values()]
                window_item.find_element('status').update('运行正常')
            except decimal.InvalidOperation:
                window_item.find_element('status').update('输入数值无效！')
                continue
            limit = [decimal.Decimal(i)
                     for i in ('17', '0.5', '0.5', '0.5', '5')]
            standard = [
                decimal.Decimal(i) for i in (
                    '8400', '60', '60', '300', '2000')]
            for i, j in zip((0, 1, 2, 3, 4), (0, 1, 1, 1, 0)):
                if numbers[i] > limit[i]:
                    num = round(numbers[i], j)
                    window_item.find_element('1' + str(i)).update(num)
                    window_item.find_element(
                        '2' +
                        str(i)).update(
                        '%.2f%%' %
                        (round(
                            num /
                            standard[i],
                            4) *
                         100))
                    window_item.find_element(
                        '3' +
                        str(i)).update(
                        '%.0f%%' %
                        (round(
                            num /
                            standard[i],
                            2) *
                         100))
                else:
                    window_item.find_element('1' + str(i)).update('0')
                    window_item.find_element('2' + str(i)).update('0%')
                    window_item.find_element('3' + str(i)).update('0%')
        elif event_n == '清空':
            for i in range(5):
                window_item.find_element('0' + str(i)).update('')
            window_item.find_element('status').update('运行正常')


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
        [sg.Button('计算', key='计算', font=('微软雅黑', 12)), sg.Button('清空', key='清空', font=('微软雅黑', 12))],
        [sg.StatusBar('运行正常', justification='center', key='status', font=('微软雅黑', 12), size=(10, 1))],
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
            window.un_hide()
            return window
        elif event_np in ['计算', '\r']:
            try:
                del values_np['status']
                numbers = [decimal.Decimal(i) for i in values_np.values()]
                window_item.find_element('status').update('运行正常')
            except decimal.InvalidOperation:
                window_item.find_element('status').update('输入数值无效！')
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
            for i, j in zip((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15),
                            (0, 1, 1, 1, 0, 1, 2, 2, 2, 1, 0, 0, 0, 1, 2, 1)):
                if numbers[i] > limit[i]:
                    num = round(numbers[i], j)
                    window_item.find_element('1' + str(i).zfill(2)).update(num)
                    window_item.find_element(
                        '2' +
                        str(i).zfill(2)).update(
                        '%.2f%%' %
                        (round(
                            num /
                            standard[i],
                            4) *
                         100))
                    window_item.find_element(
                        '3' +
                        str(i).zfill(2)).update(
                        '%.0f%%' %
                        (round(
                            num /
                            standard[i],
                            2) *
                         100))
                else:
                    window_item.find_element('1' + str(i).zfill(2)).update('0')
                    window_item.find_element(
                        '2' + str(i).zfill(2)).update('0%')
                    window_item.find_element(
                        '3' + str(i).zfill(2)).update('0%')
        elif event_np == '清空':
            for i in range(5):
                window_item.find_element('0' + str(i).zfill(2)).update('')
            for i in range(5, 16):
                window_item.find_element('0' + str(i).zfill(2)).update('0')
            window_item.find_element('status').update('运行正常')


def dehydration_win():
    rc_11 = [
        [sg.Text('新鲜水分', font=('微软雅黑', 12))],
        [sg.Text('本品水分', font=('微软雅黑', 12))],
        [sg.Text('限值一', font=('微软雅黑', 12))],
        [sg.Text('限值二', font=('微软雅黑', 12))],
        [sg.Text('限值三', font=('微软雅黑', 12))],
        [sg.Text('限值四', font=('微软雅黑', 12))],
        [sg.Text('限值五', font=('微软雅黑', 12))],
    ]
    rc_12 = [
        [sg.Input(key='00', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Input(key='01', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Input(key='02', size=(10, 1), default_text='0', font=('微软雅黑', 12))],
        [sg.Input(key='03', size=(10, 1), default_text='0', font=('微软雅黑', 12))],
        [sg.Input(key='04', size=(10, 1), default_text='0', font=('微软雅黑', 12))],
        [sg.Input(key='05', size=(10, 1), default_text='0', font=('微软雅黑', 12))],
        [sg.Input(key='06', size=(10, 1), default_text='0', font=('微软雅黑', 12))],
    ]
    rc_13 = [
        [sg.Text(key='10', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='11', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='12', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='13', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='14', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='15', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='16', size=(10, 1), font=('微软雅黑', 12))],
    ]
    rc_14 = [
        [sg.Text(size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='22', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='23', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='24', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='25', size=(10, 1), font=('微软雅黑', 12))],
        [sg.Text(key='26', size=(10, 1), font=('微软雅黑', 12))],
    ]
    layout = [
        [sg.Frame(layout=rc_11, title='项目', font=('微软雅黑', 12)),
         sg.Frame(layout=rc_12, title='数值', font=('微软雅黑', 12)),
         sg.Frame(layout=rc_13, title='结果(原始)', font=('微软雅黑', 12)),
         sg.Frame(layout=rc_14, title='结果(修约)', font=('微软雅黑', 12)),
         [sg.Button('计算', key='计算', font=('微软雅黑', 12)), sg.Button('清空', key='清空', font=('微软雅黑', 12))],
         [sg.StatusBar('准备就绪', justification='center', key='status', font=('微软雅黑', 12), size=(10, 1))],
         ]
    ]
    return sg.Window(
        '脱水率计算',
        layout,
        enable_close_attempted_event=True,
        element_justification='center',
        finalize=True,
        return_keyboard_events=True)


def dehydration(window):
    window.Hide()
    window_item = dehydration_win()
    while True:
        event_d, values_d = window_item.read()
        if event_d == '-WINDOW CLOSE ATTEMPTED-':
            window_item.close()
            window.un_hide()
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
            if fresh == decimal.Decimal('100'):
                result = real / decimal.Decimal('100')
            else:
                result = ((fresh - real) / (decimal.Decimal('100') - real))
            window_item.find_element('status').update(
                '脱水率：%.1f%%' % (round(result, 3) * 100))
            window_item.find_element('10').update('%.1f%%' % round(fresh, 1))
            window_item.find_element('11').update('%.1f%%' % round(real, 1))
            for i, j in zip((2, 3, 4, 5, 6), numbers[2:]):
                if numbers[i] > decimal.Decimal('0'):
                    length = valid_numbers(str(numbers[i]))
                    window_item.find_element(
                        '1' + str(i)).update(round(numbers[i] / (1 - result), 6))
                    window_item.find_element(
                        '2' + str(i)).update(round(numbers[i] / (1 - result), length))
                else:
                    window_item.find_element('1' + str(i)).update('0')
                    window_item.find_element('2' + str(i)).update('0')
        elif event_d == '清空':
            for i in range(7):
                window_item.find_element('0' + str(i)).update('0')
            window_item.find_element('status').update('准备就绪')


def clipboard_win():
    rc_11 = [
        [sg.Text('微生物🔺备注', font=('微软雅黑', 12))],
        [sg.Text('酒精度限值', font=('微软雅黑', 12))],
        [sg.Text('761 666检测限', font=('微软雅黑', 12))],
        [sg.Text('761 DDT检测限', font=('微软雅黑', 12))],
        [sg.Text('5009.19 666检测限', font=('微软雅黑', 12))],
        [sg.Text('5009.19 DDT检测限', font=('微软雅黑', 12))],
        [sg.Text('格式标签-预包装', font=('微软雅黑', 12))],
        [sg.Text('格式标签-非预包装', font=('微软雅黑', 12))],
        [sg.Text('详细标签-实物', font=('微软雅黑', 12))],
        [sg.Text('详细标签-电子版', font=('微软雅黑', 12))],
        [sg.Text('详细标签-无许可证电子版', font=('微软雅黑', 12))],
        [sg.Text('详细标签-非预包装电子版', font=('微软雅黑', 12))],
        [sg.Text('详细标签-非预包装实物版', font=('微软雅黑', 12))],
        [sg.Text('详细标签-样版标签', font=('微软雅黑', 12))],
    ]
    rc_12 = [
        [sg.Button('copy', key='00', font=('微软雅黑', 8))],
        [sg.Button('copy', key='01', font=('微软雅黑', 8))],
        [sg.Button('copy', key='02', font=('微软雅黑', 8))],
        [sg.Button('copy', key='03', font=('微软雅黑', 8))],
        [sg.Button('copy', key='04', font=('微软雅黑', 8))],
        [sg.Button('copy', key='05', font=('微软雅黑', 8))],
        [sg.Button('copy', key='06', font=('微软雅黑', 8))],
        [sg.Button('copy', key='07', font=('微软雅黑', 8))],
        [sg.Button('copy', key='08', font=('微软雅黑', 8))],
        [sg.Button('copy', key='09', font=('微软雅黑', 8))],
        [sg.Button('copy', key='10', font=('微软雅黑', 8))],
        [sg.Button('copy', key='11', font=('微软雅黑', 8))],
        [sg.Button('copy', key='12', font=('微软雅黑', 8))],
        [sg.Button('copy', key='13', font=('微软雅黑', 8))],
    ]
    layout = [[sg.Frame(layout=rc_11, title='内容', font=('微软雅黑', 12)), sg.Frame(
        layout=rc_12, element_justification='center', title='操作', font=('微软雅黑', 12))], ]
    return sg.Window(
        '常用剪贴板',
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
            window.un_hide()
            return window
        elif event_d in [str(i).zfill(2) for i in range(14)]:
            pyperclip.copy(TEXT[event_d])


def main():
    sg.theme('BlueMono')
    window = home()
    while True:
        event, values = window.read()
        if event is None:
            break
        elif event == '营养成分表(基础)':
            window = nutrition(window)
        elif event == '营养成分表(详细)':
            window = nutrition_plus(window)
        elif event == '脱水率计算':
            window = dehydration(window)
        elif event == '常用剪贴板':
            window = clipboard(window)


if __name__ == '__main__':
    main()
