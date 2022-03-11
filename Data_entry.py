import re
import webbrowser

import PySimpleGUI as sg
import pandas as pd
import pyperclip
import xlrd


def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]

    return inner


class PHDI:
    def __init__(self):
        self.template = [
            "抽样位置：%s\n器具名称：%s\n%s",
            "抽样位置：%s\n员工名字：%s",
            "沙拉名称：%s\n抽样位置：%s\n%s\n新鲜蔬菜原料信息：\n原料名称及生产日期：%s",
            "抽样位置：%s\n型号：%s\n紫外灯%s\n紫外灭菌灯更换时间：%s\n滤芯更换时间：%s\n%s\n水龙头%s滤网\n水龙头内%s\n最近一次消毒时间：%s",
            "抽样位置：%s\n型号：%s\n紫外灯%s\n紫外灭菌灯更换时间：%s\n滤芯更换时间：%s\n%s\n水龙头%s滤网\n水龙头内%s",
            "抽样位置：%s\n%s",
            "抽样位置：%s\n%s\n制冰机清洗消毒日期：%s",
            "饮料名称：%s\n抽样位置：%s\n%s",
            "抽样位置：%s\n器具名称：%s\n%s",
            "抽样位置：%s"]
        self.link_1 = {
            '1': '餐区桌面',
            '2': '餐区服务柜',
            '3': '生产区保洁柜/碗柜',
            '4': '清洗区',
            '5': '四门冰箱',
        }
        self.link_2 = {
            '1': '不锈钢格',
            '2': '待用冰铲',
        }
        self.link_3 = {
            '1': '已消毒好待用中',
            '2': '抽检时即时消毒',
        }
        self.people_1 = {
            '1': '汉堡工作台',
            '2': '沙拉工作台',
            '3': '水吧工作台',
        }
        self.sala_1 = {
            '1': '缤纷蔬菜沙拉',
            '2': '水果沙拉',
            '3': '美式鸡肉凯撒沙拉',
        }
        self.sala_2 = {
            '1': '柜台区冰箱',
            '2': '四门冰箱',
            '3': '小吃位',
            '4': '水吧位',
            '5': '精加工间',
        }
        self.sala_3 = {
            '1': '预制好待售',
            '2': '抽检时即时制作',
        }
        self.water_1 = {
            '1': 'KFC沙拉制作台/PP台',
            '2': '水吧',
            '3': '精加工间',
            '4': 'DOUGH房',
            '5': '腌制区',
            '6': '紫外灯后阀门',
        }
        self.water_2 = {
            '1': '沁园',
            '2': '沁园QG-U4-10',
        }
        self.water__1 = {
            '1': '洗手间',
            '2': '拖把池',
        }
        self.ice_1 = {
            '1': '制冰机',
            '2': '饮料机',
        }
        self.ice_2 = {
            '1': '冰铲存放在储冰槽内',
            '2': '冰铲存放在储冰槽外，浸泡在冰水中',
            '3': '冰铲存放在储冰槽外，未浸泡在冰水中',
        }
        self.drinks_1 = {
            '1': '嗨杯鲜果茶（冷）',
            '2': '尊赏奶茶（冷）',
            '3': '冰柠檬红茶',
        }
        self.drinks_2 = {
            '1': '柜台果汁机、饮料机',
            '2': '水吧位',
        }
        self.drinks_3 = {
            '1': '预制好待售',
            '2': '抽检时即时制作',
        }
        self.tableware_1 = {
            '1': '餐盘',
            '2': '餐碗',
            '3': '刀叉',
            '4': '勺',
            '5': '杯子',
        }
        self.ion_0 = (
            '不锈钢格',
            '儿童套餐',
            '玻璃杯',
        )
        self.ion_1 = {
            '1': '餐区桌面',
            '2': '餐区服务柜',
            '3': '生产区保洁柜/碗柜',
            '4': '水吧位',
            '5': '精加工间',
            '6': '大厅',
            '7': '清洗区',
        }
        self.tip = None

    def set_tip(self):
        link_1 = '\n'.join(f'{x[0]} {x[1]}' for x in self.link_1.items())
        link_2 = '\n'.join(f'{x[0]} {x[1]}' for x in self.link_2.items())
        link_3 = '\n'.join(f'{x[0]} {x[1]}' for x in self.link_3.items())
        people_1 = '\n'.join(f'{x[0]} {x[1]}' for x in self.people_1.items())
        sala_1 = '\n'.join(f'{x[0]} {x[1]}' for x in self.sala_1.items())
        sala_2 = '\n'.join(f'{x[0]} {x[1]}' for x in self.sala_2.items())
        sala_3 = '\n'.join(f'{x[0]} {x[1]}' for x in self.sala_3.items())
        water_1 = '\n'.join(f'{x[0]} {x[1]}' for x in self.water_1.items())
        water_2 = '\n'.join(f'{x[0]} {x[1]}' for x in self.water_2.items())
        water__1 = '\n'.join(f'{x[0]} {x[1]}' for x in self.water__1.items())
        ice_1 = '\n'.join(f'{x[0]} {x[1]}' for x in self.ice_1.items())
        ice_2 = '\n'.join(f'{x[0]} {x[1]}' for x in self.ice_2.items())
        drinks_1 = '\n'.join(f'{x[0]} {x[1]}' for x in self.drinks_1.items())
        drinks_2 = '\n'.join(f'{x[0]} {x[1]}' for x in self.drinks_2.items())
        drinks_3 = '\n'.join(f'{x[0]} {x[1]}' for x in self.drinks_3.items())
        tableware_1 = '\n'.join(
            f'{x[0]} {x[1]}' for x in self.tableware_1.items())
        ion_1 = '\n'.join(f'{x[0]} {x[1]}' for x in self.ion_1.items())
        self.tip = [
            f"{' 环节涂抹 '.center(40, '*')}\n抽样位置：\n{link_1}\n名称：\n{link_2}\n消毒状态：\n{link_3}",
            f"{' 手部涂抹 '.center(40, '*')}\n抽样位置：\n{people_1}\n员工姓名：",
            f"{' 沙拉 '.center(40, '*')}\n沙拉名称：\n{sala_1}\n抽样位置：\n{sala_2}\n产品状态：\n{sala_3}\n原料名称及生产日期（顿号分割）：",
            f"{' 过滤水 '.center(40, '*')}\n抽样位置：\n{water_1}\n过滤系统信息：\n型号：\n{water_2}\n紫外灯是否开启：1是 | "
            f"2否\n紫外灯更换日期：\n滤芯更换日期：\n近一周内是否停水停电或故障：2否\n水龙头是否有滤网：1是 | 2否\n水龙头内是否干净无垢：1是 | 2否\n最后一次消毒时间（仅限新店）：",
            f"{' 原水 '.center(40, '*')}\n抽样位置：\n{water__1}\n是否二次供水：1是 | 2否",
            f"{' 冰块 '.center(40, '*')}\n抽样位置：\n{ice_1}\n冰铲存放：\n{ice_2}\n制冰机清洗消毒日期：",
            f"{' 饮料 '.center(40, '*')}\n饮料名称：\n{drinks_1}\n抽样位置：\n{drinks_2}\n产品状态：\n{drinks_3}",
            f"{' 复用餐饮具 '.center(40, '*')}\n抽样位置：\n{link_1}\n器具名称：\n{tableware_1}\n消毒状态：\n{link_3}",
            f'{" 阴离子洗涤剂（不锈钢格）".center(30, "*")}\n抽样位置：\n{ion_1}',
            f'{" 阴离子洗涤剂（儿童套餐）".center(30, "*")}\n抽样位置：\n{ion_1}',
            f'{" 阴离子洗涤剂（玻璃杯）".center(30, "*")}\n抽样位置：\n{ion_1}',
        ]

    @staticmethod
    def date(cache):
        if not cache:
            return None, None
        if not re.match(r'\d{8}$', cache):
            return False, '进店时间错误'
        return True, f'进店时间：{cache[:2]}:{cache[2:4]}~{cache[4:6]}:{cache[6:8]}'

    def link(self, cache):
        if not cache:
            return None, None
        cache = cache.replace(' ', '').replace('，', ',').split(',')
        if len(cache) != 3 or not all(cache):
            return False, '输入内容格式错误'
        cache[0] = self.link_1.get(cache[0], cache[0])
        cache[1] = self.link_2.get(cache[1], cache[1])
        cache[2] = self.link_3.get(cache[2], cache[2])
        return True, self.template[0] % tuple(cache)

    def people(self, cache):
        if not cache:
            return None, None
        cache = cache.replace(' ', '').replace('，', ',').split(',')
        if len(cache) != 2 or not all(cache):
            return False, '输入内容格式错误'
        if not re.match(r'[\u4e00-\u9fa5]+$', cache[1]):
            return False, '员工姓名错误'
        cache[0] = self.people_1.get(cache[0], cache[0])
        return True, self.template[1] % tuple(cache)

    def sala(self, cache):
        if not cache:
            return None, None
        cache = cache.replace(' ', '').replace('，', ',').split(',')
        if len(cache) != 4 or not all(cache):
            return False, '输入内容格式错误'
        cache[0] = self.sala_1.get(cache[0], cache[0])
        cache[1] = self.sala_2.get(cache[1], cache[1])
        cache[2] = self.sala_3.get(cache[2], '产品制作时间：' + cache[2])
        if len(cache[2]) > 7 and not re.match(r'产品制作时间：\d{8}$', cache[2]):
            return False, '产品制作时间错误'
        x = cache[3].split('、')
        for y in x:
            if not re.match(r'[\u4e00-\u9fa5]+\d{8}$', y):
                return False, '原料名称及生产日期格式错误'
        return True, self.template[2] % tuple(cache)

    def water_new(self, cache):
        if not cache:
            return None, None
        cache = cache.replace(' ', '').replace('，', ',').split(',')
        if not all(cache) or len(cache) != 9:
            return False, '输入内容格式错误'
        for i in (cache[3], cache[4], cache[8]):
            if not re.match(r'\d{8}$', i):
                return False, '日期格式错误'
        cache[0] = self.water_1.get(cache[0], cache[0])
        cache[1] = self.water_2.get(cache[1], cache[1])
        cache[2] = '开启' if cache[2] == '1' else '关闭'
        cache[5] = '近一周内无停水停电、无故障' if cache[5] == '2' else cache[5]
        cache[6] = '有' if cache[6] == '1' else '无'
        cache[7] = '干净无垢' if cache[7] == '1' else '非干净无垢'
        return True, self.template[3] % tuple(cache)

    def water_old(self, cache):
        if not cache:
            return None, None
        cache = cache.replace(' ', '').replace('，', ',').split(',')
        if not all(cache) or len(cache) != 8:
            return False, '输入内容格式错误'
        for i in (cache[3], cache[4]):
            if not re.match(r'\d{8}$', i):
                return False, '日期格式错误'
        cache[0] = self.water_1.get(cache[0], cache[0])
        cache[1] = self.water_2.get(cache[1], cache[1])
        cache[2] = '开启' if cache[2] == '1' else '关闭'
        cache[5] = '近一周内无停水停电、无故障' if cache[5] == '2' else cache[5]
        cache[6] = '有' if cache[6] == '1' else '无'
        cache[7] = '干净无垢' if cache[7] == '1' else '非干净无垢'
        return True, self.template[4] % tuple(cache)

    def water_(self, cache):
        if not cache:
            return None, None
        cache = cache.replace(' ', '').replace('，', ',').split(',')
        if len(cache) != 2 or not all(cache):
            return False, '输入内容格式错误'
        cache[0] = self.water__1.get(cache[0], cache[0])
        cache[1] = '二次供水' if cache[1] == '1' else '非二次供水'
        return True, self.template[5] % tuple(cache)

    def ice(self, cache):
        if not cache:
            return None, None
        cache = cache.replace(' ', '').replace('，', ',').split(',')
        if len(cache) != 3 or not all(cache):
            return False, '输入内容格式错误'
        if not re.match(r'\d{8}$', cache[2]):
            return False, '制冰机清洗消毒日期错误'
        cache[0] = self.ice_1.get(cache[0], cache[0])
        cache[1] = self.ice_2.get(cache[1], cache[1])
        return True, self.template[6] % tuple(cache)

    def drinks(self, cache):
        if not cache:
            return None, None
        cache = cache.replace(' ', '').replace('，', ',').split(',')
        if len(cache) != 3 or not all(cache):
            return False, '输入内容格式错误'
        cache[0] = self.drinks_1.get(cache[0], cache[0])
        cache[1] = self.drinks_2.get(cache[1], cache[1])
        cache[2] = self.drinks_3.get(cache[2], cache[2])
        return True, self.template[7] % tuple(cache)

    def tableware(self, cache):
        if not cache:
            return None, None
        cache = cache.replace(' ', '').replace('，', ',').split(',')
        if len(cache) != 3 or not all(cache):
            return False, '输入内容格式错误'
        cache[0] = self.link_1.get(cache[0], cache[0])
        cache[1] = self.tableware_1.get(cache[1], cache[1])
        cache[2] = self.link_3.get(cache[2], cache[2])
        return True, self.template[8] % tuple(cache)

    def ion(self, cache):
        if not cache:
            return None, None
        if not re.match(r'\d$|[\u4e00-\u9fa5]+$', cache):
            return False, '输入内容格式错误'
        info = self.ion_1.get(cache, cache)
        return True, self.template[9] % info


class KFC(PHDI):
    def __init__(self):
        super().__init__()
        self.template[8] = "抽样位置：%s\n设备型号：%s\n设备最近一次拆机消毒日期：%s\n抽检时%s添加隔夜奶浆\n%s"
        self.link_2 = {
            '1': '不锈钢格',
            '2': '鸡夹',
            '3': '不锈钢勺',
            '4': '冰铲',
        }
        self.drinks_1 = {
            '1': '半柠半桔果茶',
            '2': '九珍果汁',
            '3': '雪顶咖啡',
        }
        self.milk_1 = {
            '1': '左', '2': '中', '3': '右'
        }
        self.milk_2 = {
            '1': '泰勒8757',
            '2': '泰勒C716/C708',
            '3': 'carpigiany',
        }
        self.ion_0 = (
            '不锈钢格',
            '酱枪筒',
        )
        self.ion_1 = {
            '1': '水吧位',
            '2': '精加工间',
            '3': '总配',
            '4': '清洗区',
            '5': '厨房',
            '6': '大厅',
        }

    def set_tip(self):
        link_1 = '\n'.join(f'{x[0]} {x[1]}' for x in self.link_1.items())
        link_2 = '\n'.join(f'{x[0]} {x[1]}' for x in self.link_2.items())
        link_3 = '\n'.join(f'{x[0]} {x[1]}' for x in self.link_3.items())
        people_1 = '\n'.join(f'{x[0]} {x[1]}' for x in self.people_1.items())
        sala_1 = '\n'.join(f'{x[0]} {x[1]}' for x in self.sala_1.items())
        sala_2 = '\n'.join(f'{x[0]} {x[1]}' for x in self.sala_2.items())
        sala_3 = '\n'.join(f'{x[0]} {x[1]}' for x in self.sala_3.items())
        water_1 = '\n'.join(f'{x[0]} {x[1]}' for x in self.water_1.items())
        water_2 = '\n'.join(f'{x[0]} {x[1]}' for x in self.water_2.items())
        water__1 = '\n'.join(f'{x[0]} {x[1]}' for x in self.water__1.items())
        ice_1 = '\n'.join(f'{x[0]} {x[1]}' for x in self.ice_1.items())
        ice_2 = '\n'.join(f'{x[0]} {x[1]}' for x in self.ice_2.items())
        drinks_1 = '\n'.join(f'{x[0]} {x[1]}' for x in self.drinks_1.items())
        drinks_2 = '\n'.join(f'{x[0]} {x[1]}' for x in self.drinks_2.items())
        drinks_3 = '\n'.join(f'{x[0]} {x[1]}' for x in self.drinks_3.items())
        milk_1 = '\n'.join(f'{x[0]} {x[1]}' for x in self.milk_1.items())
        milk_2 = '\n'.join(f'{x[0]} {x[1]}' for x in self.milk_2.items())
        ion_1 = '\n'.join(f'{x[0]} {x[1]}' for x in self.ion_1.items())
        self.tip = [
            f"{' 环节涂抹 '.center(40, '*')}\n抽样位置：\n{link_1}\n名称：\n{link_2}\n消毒状态：\n{link_3}",
            f"{' 手部涂抹 '.center(40, '*')}\n抽样位置：\n{people_1}\n员工姓名：",
            f"{' 沙拉 '.center(40, '*')}\n沙拉名称：\n{sala_1}\n抽样位置：\n{sala_2}\n产品状态：\n{sala_3}\n原料名称及生产日期（顿号分割）：",
            f"{' 过滤水 '.center(40, '*')}\n抽样位置：\n{water_1}\n过滤系统信息：\n型号：\n{water_2}\n紫外灯是否开启：1是 | "
            f"2否\n紫外灯更换日期：\n滤芯更换日期：\n近一周内是否停水停电或故障：2否\n水龙头是否有滤网：1是 | 2否\n水龙头内是否干净无垢：1是 | 2否\n最后一次消毒时间（仅限新店）：",
            f"{' 原水 '.center(40, '*')}\n抽样位置：\n{water__1}\n是否二次供水：1是 | 2否",
            f"{' 冰块 '.center(40, '*')}\n抽样位置：\n{ice_1}\n冰铲存放：\n{ice_2}\n制冰机清洗消毒日期：",
            f"{' 饮料 '.center(40, '*')}\n饮料名称：\n{drinks_1}\n抽样位置：\n{drinks_2}\n产品状态：\n{drinks_3}",
            f"{' 圣代 '.center(40, '*')}\n抽样位置：\n{milk_1}\n设备型号：\n{milk_2}\n设备最近一次拆机消毒日期：\n抽检时是否已经添加隔夜奶浆：1是 | "
            f"2否\n近一周内是否停水停电或故障：2否",
            f'{" 阴离子洗涤剂（不锈钢格）".center(30, "*")}\n抽样位置：\n{ion_1}',
            f'{" 阴离子洗涤剂（酱枪筒）".center(30, "*")}\n抽样位置：\n{ion_1}',
        ]

    def milk(self, cache):
        if not cache:
            return None, None
        cache = cache.replace(' ', '').replace('，', ',').split(',')
        if len(cache) != 5 or not all(cache):
            return False, '输入内容格式错误'
        if not re.match(r'\d{8}$', cache[2]):
            return False, '设备最近一次拆机消毒日期错误'
        cache[0] = self.milk_1.get(cache[0], cache[0])
        cache[1] = self.milk_2.get(cache[1], cache[1])
        cache[3] = "没有" if cache[3] == '2' else "已经"
        cache[4] = '近一周内无停水停电、无故障' if cache[4] == '2' else cache[4]
        return True, self.template[8] % tuple(cache)


class CJ(PHDI):
    def __init__(self):
        super().__init__()
        self.template[2] = "抽样位置：%s\n产品名称：%s"
        self.template[6] = "制冰机清洗消毒日期：%s\n%s"
        self.link_2[str(len(self.link_2) + 1)] = '打奶钢'
        self.water_2[str(len(self.water_2) + 1)] = '3M'
        self.drinks_1[str(len(self.drinks_1) + 1)] = '冰美式'
        self.drinks_1[str(len(self.drinks_1) + 1)] = '冰拿铁'

    def set_tip(self):
        link_1 = '\n'.join(f'{x[0]} {x[1]}' for x in self.link_1.items())
        link_2 = '\n'.join(f'{x[0]} {x[1]}' for x in self.link_2.items())
        link_3 = '\n'.join(f'{x[0]} {x[1]}' for x in self.link_3.items())
        people_1 = '\n'.join(f'{x[0]} {x[1]}' for x in self.people_1.items())
        water_1 = '\n'.join(f'{x[0]} {x[1]}' for x in self.water_1.items())
        water_2 = '\n'.join(f'{x[0]} {x[1]}' for x in self.water_2.items())
        ice_2 = '\n'.join(f'{x[0]} {x[1]}' for x in self.ice_2.items())
        drinks_1 = '\n'.join(f'{x[0]} {x[1]}' for x in self.drinks_1.items())
        drinks_2 = '\n'.join(f'{x[0]} {x[1]}' for x in self.drinks_2.items())
        drinks_3 = '\n'.join(f'{x[0]} {x[1]}' for x in self.drinks_3.items())
        tableware_1 = '\n'.join(
            f'{x[0]} {x[1]}' for x in self.tableware_1.items())
        self.tip = [
            f"{' 环节涂抹 '.center(40, '*')}\n抽样位置：\n{link_1}\n名称：\n{link_2}\n消毒状态：\n{link_3}",
            f"{' 手部涂抹 '.center(40, '*')}\n抽样位置：\n{people_1}\n员工姓名：",
            f"{' 蛋糕 '.center(40, '*')}\n抽样位置：\n产品名称：",
            f"{' 过滤水 '.center(40, '*')}\n抽样位置：\n{water_1}\n过滤系统信息：\n型号：\n{water_2}\n紫外灯是否开启：1是 | "
            f"2否\n紫外灯更换日期：\n滤芯更换日期：\n近一周内是否停水停电或故障：2否\n水龙头是否有滤网：1是 | 2否\n水龙头内是否干净无垢：1是 | 2否\n最后一次消毒时间（仅限新店）：",
            f"{' 冰块 '.center(40, '*')}\n制冰机清洗消毒日期：\n冰铲存放：\n{ice_2}",
            f"{' 饮料 '.center(40, '*')}\n饮料名称：\n{drinks_1}\n抽样位置：\n{drinks_2}\n产品状态：\n{drinks_3}",
            f"{' 复用餐饮具 '.center(40, '*')}\n抽样位置：\n{link_1}\n器具名称：\n{tableware_1}\n消毒状态：\n{link_3}",
        ]

    def cake(self, cache):
        if not cache:
            return None, None
        cache = cache.replace(' ', '').replace('，', ',').split(',')
        if len(cache) != 2 or not all(cache):
            return False, '输入内容格式错误'
        for i in cache:
            if not re.match(r'[\u4e00-\u9fa5]+$', i):
                return False, '输入内容含有非中文字符'
        return True, self.template[2] % tuple(cache)

    def ice(self, cache):
        if not cache:
            return None, None
        cache = cache.replace(' ', '').replace('，', ',').split(',')
        if len(cache) != 2 or not all(cache):
            return False, '输入内容格式错误'
        if not re.match(r'\d{8}$', cache[0]):
            return False, '制冰机清洗消毒日期错误'
        cache[1] = self.ice_2.get(cache[1], cache[1])
        return True, self.template[6] % tuple(cache)


@singleton
class GUI:
    VERSION = 'V0.1.0'
    ION = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\xc8\x00\x00\x00\xc8\x08\x06\x00\x00\x00\xadX\xae\x9e\x00' \
          b'\x00\x00\x01sRGB\x00\xae\xce\x1c\xe9\x00\x00\x0c\x0bIDATx^\xed\x9dO\x8c[' \
          b'W\x15\x87\xcf\xf1\xcc@\x17%\xf1\x8c\x08"\x12\x7f\x122\x9e\r\x0bR\xb1`\x85H\xc4\x02\tUUX\x82\x10\xb4jE\x89' \
          b'-\xd2\x14\x84X \xd4\xb0\x01T!5-\xb1\xa3\x88\x88\xa6\x0b\xba\xa4AU%`\x93t\x81\x84\x04\x88\x94Uk\xb7J\xaa ' \
          b'\x11E0\x9e4Hi\x92\x19\x1f\xe4\x19&$\x13\xcf\xbc{o\xees\xfc\xee\xfdf\xeb{' \
          b'\xcf}\xbf\xef\xdc\xcf\xcf\x1e??\xab\xf0\x07\x01\x08lJ@a\x03\x01\x08lN\x00A\xd8\x1d\x10\xd8\x82\x00\x82' \
          b'\xb0= \x80 \xec\x01\x08\x84\x11\xe0\x0c\x12\xc6\x8dY\x99\x10@\x90L\x1aM\xcc0\x02\x08\x12\xc6\x8dY\x99\x10' \
          b'@\x90L\x1aM\xcc0\x02\x08\x12\xc6\x8dY\x99\x10@\x90L\x1aM\xcc0\x02\x08\x12\xc6\x8dY\x99\x10@\x90L\x1aM' \
          b'\xcc0\x02\x08\x12\xc6\x8dY\x99\x10@\x90L\x1aM\xcc0\x02\x08\x12\xc6\x8dY\x99\x10@\x90L\x1aM\xcc0\x02\x08' \
          b'\x12\xc6\x8dY\x99\x10@\x90L\x1aM\xcc0\x02\x08\x12\xc6\x8dY\x99\x10@\x90L\x1aM\xcc0\x02\x08\x12\xc6\x8dY' \
          b'\x99\x10@\x90L\x1aM\xcc0\x02\x08\x12\xc6\x8dY\x99\x10@\x90L\x1aM\xcc0\x02\x08\x12\xc6\x8dY\x99\x10@\x90L' \
          b'\x1aM\xcc0\x02\x08\x12\xc6\x8dY\x99\x10@\x90L\x1aM\xcc0\x02\x08\x12\xc6\x8dY\x99\x10@\x90L\x1aM\xcc0\x02' \
          b'\x08\x12\xc6\x8dY\x99\x10@\x90L\x1aM\xcc0\x02\x08\x12\xc6\x8dY\x99\x10@\x90L\x1aM\xcc0\x02\x08\x12\xc6' \
          b'\x8dY\x99\x10@\x90L\x1aM\xcc0\x02\x08\x12\xc6\x8dY\x99\x10@\x90L\x1aM\xcc0\x02\x08\x12\xc6\x8dY\x99\x10' \
          b'@\x90L\x1aM\xcc0\x02\x08\x12\xc6\x8dY\x99\x10@\x90L\x1aM\xcc0\x02\xce\x82\xcc\xbd\xd0\xdbvszj\xe7\xb4' \
          b'\xc8GLW\xa6\xc2\x96c\x16\x04\xee\x1f\x01\xb5\xa9\x95e\x91\xcb3\xcb+\xff\\<\xd4x\xcf\xe5H\xb6\x14d\xeeX' \
          b'\xef\xd3\xa6\xfa\rU\xfb\x8a\x884\\\n2\x06\x02\x95 `\xd25\x91\xdf,' \
          b'OO\xbft\xf5\xc9\xddonv\xcc#\x05\xd9v\xf2\xe2\xdc\xd4\x8dk?\x15\xd3\'T\xa5V\x89\xc0\x1c$\x04\x02\x08\x98' \
          b'\xc8\x8a\x88udj\xeaG\xfd\'\xf7\\\xd9X\xe2.A\xb6\x1d\xeb~nJ\xf5UU\xd9\x11\xb0\x1eS ' \
          b'PI\x02&r\xd1\xcc\x1eYj-\x9c\xbb=\xc0\x1d\x82\xccv\xba_S\xd1_W2!\x07\r\x81\x08\x04Lj\x0f\xf7\x9b{^[' \
          b'/uK\x90\xed\xc7\xde\xf9b\xad6\xf8\xbd\x8a\xf0\x06<\x02hJT\x94\x80\xc9\xb5\x15\xd5\xcf_i\xce\xffu\x98`U' \
          b'\x90\x0f\x9dx\xeb\xc33\xcbz^T\x1f\xach,' \
          b'\x0e\x1b\x02\xf1\x08\x98\\Z\xbc\xfe\xc0\xa7\xe4\xbb\x1f\xbf\xb6*H\xbd\xdd\xfbyM\xe5{' \
          b'\xf1V\xa0\x12\x04\xaaM\xc0\xcc~\xd0o-<\xab\xc3\xffXM\xdfx\xff\xdf\xd5\x8e\xc3\xd1C ' \
          b'.\x01\x13\xfbW\xbf\xb9\xb0C\xe7\xda\xbd\xc7E\xe5d\xdc\xf2T\x83@\xf5\t\x98\xe8\x97u\xb6\xd3}UE\x1f\xae' \
          b'~\x1c\x12@ .\x013;\xa1\xb3\xed^OU\xe6\xe3\x96\xa6\x1a\x04\x92 \xf0\'\x9d\xed\xf4\x96Td{' \
          b'\x12q\x08\x01\x81\x98\x04L.\xe9\\\xa7g\x9e5\xdf7\xd5\xc7L\xec\x92\xe7<\x86C\xe0\xbe\x11\xd0\x81\xedT\xd5' \
          b'\x97}\x0f\xc0[\x10\x13\xfbE\xbf\xb9p\xc8w!\xc6C\xe0~\x13\x98\xed\xbc}\\\xc5\xbe\xeds\x1c\xde\x82\x88\xc9' \
          b'\x8f\x17[\x8d#>\x8b0\x16\x02\x93@`\xae\xdd;"*\xcf\xf8\x1c\x0b\x82\xf8\xd0bl\xa5\t ' \
          b'H\xa5\xdb\xc7\xc1\x97M\x00A\xca&L\xfdJ\x13@\x90J\xb7\x8f\x83/\x9b\x00\x82\x94M\x98\xfa\x95&\x80 ' \
          b'\x95n\x1f\x07_6\x01\x04)\x9b0\xf5+M\x00A*\xdd>\x0e\xbel\x02\x08R6a\xeaW\x9a\x00\x82T\xba}\x1c|\xd9\x04' \
          b'\x10\xa4l\xc2\xd4\xaf4\x01\x04\xa9t\xfb8\xf8\xb2\t ' \
          b'H\xd9\x84\xa9_i\x02\x13+\xc8\\\xbb\xfb\xa2\xa8>z\xaft\x07f\x8f-\xb5\x16N\x15\xd5\xa9wz\x87k"\xcf\x15\x8d' \
          b'+z| \xf2\xf4R\xb3q\xb4h\\\xbd\xdd}\xb4\xa6\xfab\xd1\xb8\xc2\xc7\xcdN-\xb6\x16\x1e+\x1aW?\xde\xdb\xa7' \
          b'\x03yEU\xeaEc\xb7z\xdcDN\xf7\x9b\x8d\xe1}\x97\xb7\xfc\xab\xb7\xbb{' \
          b'U\xf4\xcc=\xafgv\xcen\xcc\xec_zz\xf7\xd2\xc6\x05\xbd\xd7pdu\xfb:\x93+\x88\xff\x97\xb2F6\xccD^\xef7\x1b' \
          b'\xfb\x8a\x1a:\xdb\xe9\x9dU\x91/\x14\x8d+z\xdc\xc4.\xf4\x9b\x0b\xbb\x8b\xc6\xc5Zo\xb8\xceb\xb3Qx\xc7\xfd' \
          b'\x90Fo\x96a\xa0\xd3\xbb\x97\x0e\xee\xbe\xb0U\xc6\xb8\xeb\xc9\xfe\xa5\x83\x8d\xb3\x1b\xd7\x0bY\xc3\x85\x15' \
          b'\x82\x8c\xe8\xec\xb87\xec\xb8\xd7\x0b\xd9L\x9b\x0b2z\xc3\xde\xeb\xc6\xf2]/$\x13\x82l\xa0<\xee3\x88\xeb3' \
          b':\x82\x14\x9dc\xff\xff\xf8@9\x83\xdcE+\xe0{' \
          b'\xef\x13\xf1\x12\x0bA\xd6\xda\x10\xf2\xec\xce\x19\xc4\xfdIC\x10\xc4\x1d\x96\xcb\xcb\x86qlX^b\xad\x11\x18' \
          b'\xcbWn\x11\x04A\xd6\t\xf0\x12k\xc4^@\x10\x04A\x90-\xf6\x00\x82 \x08\x82 ' \
          b'\xc8=\x7f\xee\xe2\xfaO\x01\xde\x83\xacm6\x97\xf7k\xf7\xfa^\x8a\xf7 [' \
          b'\x88m"W\xfa\xcdF\xe1\xa7\xd5\x95\xfe7\xaf\xd9C\x1b\x7f\x97o#\x92q\x08\x19\xb2F2\x82\xccv\xba\xe7T\xf43' \
          b'\xee/46\x19i\xfa\xfcbk\xfepQ\x9d\xb9N\xf7\x94\x88~\xb3h\\\xf1\xe3\xf6\xd2bs\xa1\xf0\x12\x99\xb9\xf6\xdbGE' \
          b'\xed\xa9\xe2z[\x8f0\xb17\xfa\xcd\x85\xbdEub]\xdab&\xef\xf6[\x8d]\x85\xebu\xde>P\x13{' \
          b'\xa5h\\\xd1\xe3\xc3\'\x1c\xd3\xe9\xbd\xa3>\xb9\xcfZ\x90\xfas\xe7\xeb\xf2\x81\x9b\x07j\xa2\x85\xcd\xd8\x0c' \
          b'\xf2@\xf5\xdcRs\xfetQ\x13\xd6\x1f\xaf\x0f\x9bjV\xb8\xd9&f=\xb1\x0brc\xe6\xf4\xa8\xeb\x94F\x1d\xe3\xf0\xda' \
          b'\xa5\x9a\xe8\x01W\x1e\x1b\xc7\r\xc6\xbd\x9e\xca\x92\xe8\xf4\xe9\xcd.k\xc9Z\x90\xd0&2/\x1f\x02\x08\x92O' \
          b'\xafI\x1a@\x00A\x02\xa01%\x1f\x02\x08\x92O\xafI\x1a@\x00A\x02\xa01%\x1f\x02\x08\x92O\xafI\x1a@\x00A\x02' \
          b'\xa01%\x1f\x02\x08\x92O\xafI\x1a@ \xe4\xc3\xd6d>I\x1f\xf2\xaawzn\xd7*\xe9\xf4\xbbE\xdf\x91\xde\x8c?k\xb8' \
          b'\xef\xcc2X\xad~ \xfc\xc1\xe5\x80+&t\x97\x9a\x1d\xf5\xbd)D2\x82\xccvzgT\xa4\xf0f\x0b\xeb\xed\xdd\xec;\x03[' \
          b'\xb5\x9f5\xdc\xe5(\x8b\xd5l\xbb\xfb7U\r\xbez\xc1=\xc1\xda\xc8d\x04\xf1\xbe\xdc=\xe0\x87BY\xc3}{' \
          b'\x95\xc5\xca\xbb\xae\xfb!\x8f\x1c\x89 ' \
          b'\x1e\x00\xbd\x9b\x83\x84\xeet\x1dYy\xf7\xc0\xfd\x08\x10\xe4\x0e\x02\x8e\r\xb9}\x8ewsX\xc3}{' \
          b':\xb2\xf2\xee\x81\xfb\x11 \x08\x82\xac\x11\xf0\xded\x8e\x9bw\x1cO&\xde\xc7\x8e \xd5o\xfa86V*k ' \
          b'\xc8\xb0\x93\x13\xf4\x8c\x95\xca\xc6J%\x07\x82 ' \
          b'\x88y\xbd*\xc8\xec\xc9d\x9c\x82\xb8~\xfb\xf2\x8e\'\x9fv\xef\x88\xa8<\xe3\xd3\xc3\xc9\xfcNzf\x1b\x8b3\x88' \
          b'\xcf\x96]\x1b\xebz\xe7}\x04\xf9\x1f\x01\xefg/$t\xdf\x95\x8e\xac\xbc{' \
          b'\xe0~\x04\x1b\xfe\x87co\xd8\xf5\x99}\xae_O^\x9f\x1cr\xbd\x17g\x10\x8f&yo\x00\xc7\x8d\xc5\x19\xc4\xbd\t' \
          b'\xc3\x1bM\x98\xd8\x81\xa2;\xb1\x8c\xaa8\xb1\x82\xf8\xde\x16\'\xf0R\x13\xaf\xdf\x04a\r\xf7\xdfOqe\x15\xed' \
          b'\xee5#v\xf7\xf0\x8e(*vzp}\xe6\xb0\xef\x99c\xe2\xcf ' \
          b'\xc3\x03\x1c\xfe*\x92\xdb\xf3\xc4\xf4\x85\xe0\x8b\x15Y\xc3\rqI\xfdX\xbdX\xf1\x81\xe5R\xae\xc5\x1a\xf5\xa3' \
          b';\xcea\xd7_\x86O\xea\x9bt\xdf \x8c\x87@\x19\x04&\xf6%V\x19a\xa9\t\x01_\x02\x08\xe2K\x8c\xf1Y\x11@\x90\xac' \
          b'\xdaMX_\x02\x08\xe2K\x8c\xf1Y\x11@\x90\xac\xdaMX_\x02\x08\xe2K\x8c\xf1Y\x11@\x90\xac\xdaMX_\x02\x08\xe2K' \
          b'\x8c\xf1Y\x11@\x90\xac\xdaMX_\x02\x08\xe2K\x8c\xf1Y\x11\x98hA\xca\xb8Q\xd9\xc6\xee:\xaf\x91\xd5\xb6\xb83' \
          b'\xecR\xb3\xf1zH\xfc\xfa\xf1\xf3\xbb\xc4\x96?\xe92wR\xd7\x98XA\xca\xbaQ\xd9\xed\xcd\xf2]\xc3\xa5\xd1)\x8e1' \
          b'\x91\xb3\xfdfc\xbfO\xb6\xe1\x85\xa65\x933\xaes&u\x8d\x89\x15d"\xbfG\xe1\xda\xed\x04\xc7\x8d\xe3\x86k\xa9' \
          b'\xac\x91\xef\x17\xa6\x12\xdc\xf8\xae\x91R\xd9\xbc\xe3\xc8\x81 \xae\xbb*\xa1q\xe3\xd8X\xa9\xac\x81 ' \
          b'\tm|\xd7(\xa9l\xdeq\xe4@\x10\xd7]\x95\xd0\xb8ql\xacT\xd6@\x90\x846\xbek\x94T6\xef8r ' \
          b'\x88\xeb\xaeJh\xdc86V*k HB\x1b\xdf5J*\x9bw\x1c9\x10\xc4uW%4n\x1c\x1b+\x955\x10$\xa1\x8d\xef\x1a%\x95\xcd' \
          b';\x8e\x1cc\x11d\x12o\x1c\xe7\xba\x99R\x1bg"\xaf\xf7\x9b\r\xc7{' \
          b'\x94\xad\xa5\x0f\xb8\xd4d"\xd7\x98\xd8KM\xd6!\xbbm\xb6q\xdc8\xce\xedHR\x1c\x15z\x03\xb6\xd5\x8b\x15ey\x97' \
          b'\x0b\x93I]c\xa2\x05q\x01\xcb\x18\x08\x94I\x00A\xca\xa4K\xed\xca\x13@\x90\xca\xb7\x90\x00e\x12@\x902\xe9R' \
          b'\xbb\xf2\x04\x10\xa4\xf2-$@\x99\x04\x10\xa4L\xba\xd4\xae<\x01\x04\xa9|\x0b\tP&\x01\x04)\x93.\xb5+O\x00A' \
          b'*\xdfB\x02\x94I\x00A\xca\xa4K\xed\xca\x13@\x90\xca\xb7\x90\x00e\x12@\x902\xe9R\xbb\xf2\x04\x10\xa4\xf2-$' \
          b'@\x99\x04\xc6"\x88\x99\x1c\xeb\xb7\x1a\xdf)3\x08\xb5!P\x06\x81\xd9v\xaf\xad*M\x9f\xda!\xdf\x07\xb9\xb6"r' \
          b'\xe0J\xab\xf1\x07\x9f\x85\x18\x0b\x81\xfbI\xa0\xde\xe9=R\x13\xf9\xad\xef1\xe8\\\xbb{' \
          b'UT\x1f\xf4\x9d\xc8x\x08\xa4O\xc0\xae\xea\\\xbb\xf7\x96\xa8,' \
          b'\xa4\x1f\x96\x84\x10\xf0$`\xf6\xe6\xf0%\xd6\xefD\xe4K\x9eS\x19\x0e\x81\xe4\t\x98\xd8kZ?\xde=T3}>\xf9\xb4' \
          b'\x04\x84\x80\'\x01\x13;\xa8s/\xf4>&\xd3r\xd1s.\xc3!\x90<\x81\xeb3S\x1f\xd5a\xca\xd9v\xf7eU\xfdj\xf2\x89\t' \
          b'\x08\x01W\x02&\xbfZl5\x1e_\x15d\xfb\x89\xde\x9e\xda\xb2tU\xa5\xe6:\x9fq\x10H\x95\x80\x89\xdd\xd0e\xdd' \
          b'\xb3x\xa8\xf1\x8fUAV\xcf"\x9d\xee\xf7U\xf4\xd9TC\x93\x0b\x02\xce\x04L\xbf\xb5\xd8\x9a\xff\xe5p\xfc-A\xd6$' \
          b'\xe9\x1dS\x91\x96s!\x06B 1\x02&\xf2\x93~\xb3\xf1\xc3\xf5Xw\x08\xb2~&\x11\xd3\x9f\xf1r+\xb1\xce\x13gK\x02' \
          b'&vST\x9f\xea\x1fl\x1c\xbf}\xe0]\x82\x0c\x1f\x1c\xfe\x9c\xb2\x9a\x9cT\x95y\xb8B ' \
          b'u\x02&\xf6\xf7\x15\x9bz\xe2\xbd\xd6\x9e?o\xcc:R\x90\xf5A\xf5N\xef\xb0\x8a|]E>\x9b:$\xf2\xe5G\xc0D\xfe\xa8' \
          b'"\xa7\x16\x9b\x8d\x93\x9b\xa5\xdfR\x90[' \
          b'o\xe0O\xbc\xf3\t\xbb9xHk\xb6\xd3Lv\xd4D\xa7\xf2\xc3I\xe2\xaa\x13\x18\x88\xad\xa8\xc8e\xb1\xa9\x8b7\xa7' \
          b'\xec/\xff98\x7f\xb9(\x93\x93 EEx\x1c\x02\xa9\x12@\x90T;K\xae(\x04\x10$\nF\x8a\xa4J\x00AR\xed,' \
          b'\xb9\xa2\x10@\x90(\x18)\x92*\x01\x04I\xb5\xb3\xe4\x8aB\x00A\xa2`\xa4H\xaa\x04\x10$\xd5\xce\x92+\n\x01\x04' \
          b'\x89\x82\x91"\xa9\x12@\x90T;K\xae(\x04\x10$\nF\x8a\xa4J\x00AR\xed,\xb9\xa2\x10@\x90(' \
          b'\x18)\x92*\x01\x04I\xb5\xb3\xe4\x8aB\x00A\xa2`\xa4H\xaa\x04\x10$\xd5\xce\x92+\n\x01\x04\x89\x82\x91"\xa9' \
          b'\x12@\x90T;K\xae(\x04\x10$\nF\x8a\xa4J\x00AR\xed,\xb9\xa2\x10@\x90(' \
          b'\x18)\x92*\x01\x04I\xb5\xb3\xe4\x8aB\x00A\xa2`\xa4H\xaa\x04\x10$\xd5\xce\x92+\n\x01\x04\x89\x82\x91"\xa9' \
          b'\x12@\x90T;K\xae(\x04\x10$\nF\x8a\xa4J\x00AR\xed,\xb9\xa2\x10@\x90(' \
          b'\x18)\x92*\x01\x04I\xb5\xb3\xe4\x8aB\x00A\xa2`\xa4H\xaa\x04\x10$\xd5\xce\x92+\n\x01\x04\x89\x82\x91"\xa9' \
          b'\x12@\x90T;K\xae(\x04\x10$\nF\x8a\xa4J\x00AR\xed,\xb9\xa2\x10@\x90(' \
          b'\x18)\x92*\x01\x04I\xb5\xb3\xe4\x8aB\x00A\xa2`\xa4H\xaa\x04\x10$\xd5\xce\x92+\n\x81\xff\x02\xf1\x02\xb1' \
          b'\x93\xc9\xa6\xe6J\x00\x00\x00\x00IEND\xaeB`\x82 '
    kfc = KFC()
    phdi = PHDI()
    cj = CJ()
    [x.set_tip() for x in (kfc, phdi, cj)]
    kfc_new = (
        kfc.link,
        kfc.people,
        kfc.sala,
        kfc.water_new,
        kfc.water_,
        kfc.ice,
        kfc.drinks,
        kfc.milk,
        kfc.ion,
        kfc.ion)
    kfc_common = (
        kfc.link,
        kfc.people,
        kfc.sala,
        kfc.water_old,
        kfc.ice,
        kfc.drinks,
        kfc.milk,
        kfc.ion,
        kfc.ion)
    phdi_new = (
        phdi.link,
        phdi.people,
        phdi.sala,
        phdi.water_new,
        phdi.water_,
        phdi.ice,
        phdi.drinks,
        phdi.tableware,
        phdi.ion,
        phdi.ion,
        phdi.ion)
    phdi_common = (
        phdi.link,
        phdi.people,
        phdi.sala,
        phdi.water_old,
        phdi.ice,
        phdi.drinks,
        phdi.tableware,
        phdi.ion,
        phdi.ion,
        phdi.ion)
    cj_common = (
        cj.link,
        cj.people,
        cj.cake,
        cj.water_old,
        cj.ice,
        cj.drinks,
        cj.tableware)

    def __init__(self):
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
        sg.theme_add_new('BS_Theme', theme)
        sg.theme('BS_Theme')
        self.screen = '餐厅类型：\n1 KFC新店\n2 KFC常规\n3 PHDI新店\n4 PHDI常规\n5 C&J'
        self.type = None
        self.tip = None
        self.step = 0
        self.date = None
        self.data = []
        self.sheet = None

    def run(self):
        window = self.home()
        while True:
            event, _ = window.read(timeout=100)
            if event is None:
                break
            elif event == '表格信息录入':
                self.enter_info(window)
            elif event == '系统信息录入':
                self.copy_info(window)
            elif event == '工具使用说明':
                self.info(window)
            elif event == '获取工具源码':
                webbrowser.open(
                    'https://github.com/JoeanAmiee/Private_office_tools')
        window.close()

    def home(self):
        layout = [
            [sg.Button('表格信息录入', size=(12, None), font=('微软雅黑', 12)),
             sg.Button('系统信息录入', size=(12, None), font=('微软雅黑', 12))],
            [sg.Button('工具使用说明', size=(12, None), font=('微软雅黑', 12)),
             sg.Button('获取工具源码', size=(12, None), font=('微软雅黑', 12))],
        ]
        return sg.Window(
            f'数据录入小工具 {self.VERSION}',
            layout,
            text_justification='center',
            element_justification='center',
            icon=self.ION,
            finalize=True)

    def enter_info_gui(self):
        layout = [
            [sg.Multiline(self.screen,
                          autoscroll=True, font=('微软雅黑', 10), size=(40, 20), disabled=True,
                          key='screen')],
            [sg.Input('', key='-INPUT-', font=('微软雅黑', 10), size=(42, None))],
            [sg.StatusBar('正常运行', key='status', font=('微软雅黑', 11), size=(34, None))],
        ]
        return sg.Window(
            f'数据录入小工具 {self.VERSION}',
            layout,
            text_justification='center',
            element_justification='center',
            icon=self.ION,
            finalize=True,
            return_keyboard_events=True,
        )

    def enter_info(self, win):
        window = self.enter_info_gui()
        win.hide()
        while True:
            event, values = window.read(timeout=100)
            if event is None:
                self.reset()
                break
            elif event == '\r':
                if self.type and self.date:
                    info = self.type[self.step](values['-INPUT-'])
                    if info[0]:
                        self.data.append(info[1])
                        window.find_element('status').update('正常运行')
                    elif info[1]:
                        self.step -= 1
                        window.find_element('status').update(info[1])
                    else:
                        self.data.append(None)
                        window.find_element('status').update('正常运行')
                    del info
                    if len(self.type) - 1 == self.step:
                        self.copy(window)
                        self.reset()
                        window.find_element('screen').update(self.screen)
                    else:
                        self.step += 1
                        window.find_element('screen').update(
                            self.tip[self.step])
                elif self.type:
                    info = PHDI.date(values['-INPUT-'])
                    if info[0]:
                        self.date = info[1]
                        window.find_element('status').update('正常运行')
                        window.find_element('screen').update(
                            self.tip[self.step])
                    elif info[1]:
                        window.find_element('status').update(info[1])
                    else:
                        self.reset()
                        window.find_element('status').update('正常运行')
                        window.find_element('screen').update(self.screen)
                    del info
                elif self.shop(values['-INPUT-']):
                    window.find_element('status').update('正常运行')
                    window.find_element('screen').update('进店时间：')
                else:
                    window.find_element('status').update('店铺类型错误')
                window.find_element('-INPUT-').update('')
        win.un_hide()
        window.close()
        del window

    def shop(self, text):
        type_ = {
            '1': (self.kfc_new, self.kfc.tip),
            '2': (self.kfc_common, self.kfc.tip[:4] + self.kfc.tip[5:]),
            '3': (self.phdi_new, self.phdi.tip),
            '4': (self.phdi_common, self.phdi.tip[:4] + self.phdi.tip[5:]),
            '5': (self.cj_common, self.cj.tip),
        }
        type_ = type_.get(text, (None, None))
        if all(type_):
            self.type = type_[0]
            self.tip = type_[1]
            del type_
            return True
        del type_
        return False

    def reset(self):
        self.type = None
        self.tip = None
        self.step = 0
        self.date = None
        self.data = []
        self.sheet = None

    def copy_gui(self):
        layout = [
            [sg.Button('复制数据', font=('微软雅黑', 10))],
            [sg.Button('返回', font=('微软雅黑', 10))],
        ]
        return sg.Window(
            '',
            layout,
            keep_on_top=True,
            grab_anywhere=True,
            no_titlebar=True,
            # alpha_channel=0.5,
            text_justification='center',
            element_justification='center',
            # relative_location=(600, 0),
            icon=self.ION,
            finalize=True)

    def copy(self, win):
        window = self.copy_gui()
        win.hide()
        while True:
            event, _ = window.read(timeout=100)
            if not event or event == '返回':
                break
            elif event == '复制数据':
                self.copy_data()
        win.un_hide()
        window.close()
        del window

    def copy_data(self):
        data = []
        for x in self.data:
            if x:
                data.append(f'"{self.date}\n{x}"')
            else:
                data.append('')
        # sg.clipboard_set('\r\n'.join(data) + '\r\n')
        pyperclip.copy('\r\n'.join(data) + '\r\n')

    def copy_info_gui(self):
        layout = [
            [sg.Button('选择数据文件', font=('微软雅黑', 10))],
            [sg.Input('', size=(10, None), font=('微软雅黑', 10))],
            [sg.Button('读取餐厅数据', font=('微软雅黑', 10), disabled=True)],
            [sg.Button('环节涂抹', key='-0-', font=('微软雅黑', 10), disabled=True)],
            [sg.Button('手部涂抹', key='-1-', font=('微软雅黑', 10), disabled=True)],
            [sg.Button('沙拉', key='-2-', font=('微软雅黑', 10), disabled=True)],
            [sg.Button('过滤水', key='-3-', font=('微软雅黑', 10), disabled=True)],
            [sg.Button('冰块', key='-4-', font=('微软雅黑', 10), disabled=True)],
            [sg.Button('饮料', key='-5-', font=('微软雅黑', 10), disabled=True)],
            [sg.Button('圣代/餐饮具', key='-6-', font=('微软雅黑', 10), disabled=True)],
            [sg.Button('返回', font=('微软雅黑', 10))],
            [sg.StatusBar('正常运行', key='status', font=('微软雅黑', 10), size=(10, None))],
        ]
        return sg.Window(
            '',
            layout,
            keep_on_top=True,
            grab_anywhere=True,
            no_titlebar=True,
            # alpha_channel=0.5,
            text_justification='center',
            element_justification='center',
            # relative_location=(600, 0),
            icon=self.ION,
            finalize=True)

    def copy_info(self, win):
        window = self.copy_info_gui()
        win.hide()
        while True:
            event, values = window.read(timeout=100)
            if not event or event == '返回':
                break
            elif event == '选择数据文件':
                window.find_element('选择数据文件').update(disabled=True)
                file = self.choice_file()
                if file and self.read_xls(file):
                    window.find_element('读取餐厅数据').update(disabled=False)
                    window.find_element('status').update('正常运行')
                else:
                    self.reset()
                    self.update(window, [True for _ in range(7)])
                    window.find_element('读取餐厅数据').update(disabled=True)
                    window.find_element('status').update('读取文件失败')
                del file
                window.find_element('选择数据文件').update(disabled=False)
            elif event == '读取餐厅数据':
                try:
                    data = self.sheet[self.sheet['餐厅编号'] == values[0]]
                except TypeError:
                    continue
                if data.empty:
                    del data
                    self.reset()
                    self.update(window, [True for _ in range(7)])
                    window.find_element('status').update('未找到数据')
                    continue
                self.check_data(data.copy())
                del data
                self.update(window, [not x for x in self.data])
            elif event in ('-0-', '-1-', '-2-', '-3-', '-4-', '-5-', '-6-'):
                pyperclip.copy(self.data[int(event[1])])
        win.un_hide()
        window.close()
        del window

    def choice_file(self):
        return sg.popup_get_file(
            '',
            file_types=(
                ('XLS',
                 '*.xls'),
            ),
            icon=self.ION,
            no_window=True,
        )

    def read_xls(self, file):
        try:
            with xlrd.open_workbook(file) as sheet:
                sheet = sheet.sheet_by_name("抽检数据表")
                sheet = [
                    sheet.col_values(
                        3, 1), sheet.col_values(
                        12, 1), sheet.col_values(
                        14, 1), sheet.col_values(
                        16, 1), sheet.col_values(
                        18, 1), sheet.col_values(
                        20, 1), sheet.col_values(
                        22, 1)]
                max_ = sheet[0].index('')
                for i, j in enumerate(sheet):
                    sheet[i] = sheet[i][:max_]
                self.sheet = pd.DataFrame(
                    sheet,
                    index=(
                        '餐厅编号',
                        '备注',
                        '地点',
                        '总数',
                        '大肠',
                        '杆菌',
                        '耐热')).T
            return True
        except xlrd.biffh.XLRDError:
            return False

    @staticmethod
    def update(window, disabled: list):
        if len(disabled) != 7:
            raise ValueError('按钮布尔值数量错误！')
        for i, j in enumerate(disabled):
            window.find_element(f'-{i}-').update(disabled=j)

    def check_data(self, data):
        data.reset_index(drop=True, inplace=True)
        if data.shape[0] == 8:
            data.drop(4, axis=0, inplace=True)
        elif data.shape[0] != 7:
            raise ValueError('数据形状错误！')
        self.data = []
        for i in range(7):
            if not data.iloc[i, 1] or not data.iloc[i, 2]:
                self.data.append(False)
                continue
            if 0 in data.iloc[i, 3:].values:
                self.data.append(False)
                continue
            self.data.append(f'{data.iloc[i, 1]}\n取样地点：{data.iloc[i, 2]}')

    def info_gui(self):
        layout = [
            [sg.Text('表格信息录入', font=('微软雅黑', 12))],
            [sg.Text('输入内容后按回车键确认\n日期时间均输入八位数字\n没有合适选项时可直接输入中文\n不同选项使用逗号分隔\n不输入内容直接按回车键可跳过样品\n输入内容错误时需要重新输入\n'
                     '点击“复制数据”将内容写入剪贴板\n然后直接粘贴至表格中', font=('微软雅黑', 10))],
            [sg.Text('系统信息录入', font=('微软雅黑', 12))],
            [sg.Text('选择 XLS 格式的表格文件\n表格数据必须按顺序录入\n输入餐厅编号，点击“读取餐厅数据”\n点击样品名称可复制对应备注\n未采样或不合格样品的按钮无法点击',
                     font=('微软雅黑', 10))],
        ]
        return sg.Window(
            '工具使用说明',
            layout,
            text_justification='center',
            element_justification='center',
            icon=self.ION,
            finalize=True)

    def info(self, win):
        window = self.info_gui()
        win.hide()
        while True:
            event, _ = window.read(timeout=100)
            if event is None:
                break
        win.un_hide()
        window.close()
        del window


if __name__ == "__main__":
    GUI().run()
