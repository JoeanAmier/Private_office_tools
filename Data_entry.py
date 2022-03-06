import re

import pyperclip


class PHDI:
    def __init__(self):
        self.cache_1 = None
        self.cache_2 = None
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

    def start(self, new_=False):
        date, data = self.data(new_)
        if not date:
            return
        ion = []
        for x in data:
            if x:
                ion.append(f'"{date}\n{x}"')
            else:
                ion.append('""')
        ion = '\r\n'.join(ion) + '\r\n'
        self.cache_2 = ion
        while True:
            info = input(
                f"{'=' * 50}\n下一步：\n1 将样品数据写入剪贴板\n2 将阴离子洗涤剂数据写入剪贴板\n3 返回餐厅选择\n")
            if info == '1':
                pyperclip.copy(self.cache_1)
                print('样品数据已写入剪贴板！')
            elif info == '2':
                pyperclip.copy(self.cache_2)
                print('阴离子洗涤剂数据已写入剪贴板！')
            elif info == '3':
                break
            else:
                continue

    def date(self):
        cache = input(f"{'=' * 50}\n进店时间：")
        if not cache:
            return None
        if not re.match(r'\d{8}$', cache):
            return self.date()
        return f'进店时间：{cache[:2]}:{cache[2:4]}~{cache[4:6]}:{cache[6:8]}'

    def data(self, new_):
        if not (date := self.date()):
            return None, None
        link = self.link()
        people = self.people()
        sala = self.sala()
        water = self.water(new_)
        water_ = self.water_() if new_ else None
        ice = self.ice()
        drinks = self.drinks()
        tableware = self.tableware()
        if new_:
            _ = (link, people, sala, water, water_, ice, drinks, tableware)
        else:
            _ = (link, people, sala, water, ice, drinks, tableware)
        data = []
        for x in _:
            if x:
                data.append(f'"{date}\n{x}"')
            else:
                data.append('""')
        data = '\r\n'.join(data) + '\r\n'
        self.cache_1 = data
        ion = [self.ion(x) for x in self.ion_0]
        return date, ion

    def link(self):
        link_1 = '\n'.join(f'{x[0]} {x[1]}' for x in self.link_1.items())
        link_2 = '\n'.join(f'{x[0]} {x[1]}' for x in self.link_2.items())
        link_3 = '\n'.join(f'{x[0]} {x[1]}' for x in self.link_3.items())
        info = input(
            f"{' 环节涂抹 '.center(40, '*')}\n抽样位置：\n{link_1}\n名称：\n{link_2}\n消毒状态：\n{link_3}\n")
        if not info:
            return None
        cache = info.replace(' ', '').replace('，', ',').split(',')
        if len(cache) != 3 or not all(cache):
            return self.link()
        cache[0] = self.link_1.get(cache[0], cache[0])
        cache[1] = self.link_2.get(cache[1], cache[1])
        cache[2] = self.link_3.get(cache[2], cache[2])
        return self.template[0] % tuple(cache)

    def people(self):
        people_1 = '\n'.join(f'{x[0]} {x[1]}' for x in self.people_1.items())
        info = input(
            f"{' 手部涂抹 '.center(40, '*')}\n抽样位置：\n{people_1}\n员工姓名：\n")
        if not info:
            return None
        cache = info.replace(' ', '').replace('，', ',').split(',')
        if len(cache) != 2 or not all(cache):
            return self.people()
        cache[0] = self.people_1.get(cache[0], cache[0])
        return self.template[1] % tuple(cache)

    def sala(self):
        sala_1 = '\n'.join(f'{x[0]} {x[1]}' for x in self.sala_1.items())
        sala_2 = '\n'.join(f'{x[0]} {x[1]}' for x in self.sala_2.items())
        sala_3 = '\n'.join(f'{x[0]} {x[1]}' for x in self.sala_3.items())
        info = input(
            f"{' 沙拉 '.center(40, '*')}\n沙拉名称：\n{sala_1}\n抽样位置：\n{sala_2}\n产品状态：\n{sala_3}\n原料名称及生产日期（顿号分割）：\n")
        if not info:
            return None
        cache = info.replace(' ', '').replace('，', ',').split(',')
        if len(cache) != 4 or not all(cache):
            return self.sala()
        cache[0] = self.sala_1.get(cache[0], cache[0])
        cache[1] = self.sala_2.get(cache[1], cache[1])
        cache[2] = self.sala_3.get(cache[2], '产品制作时间：' + cache[2])
        if len(cache[2]) > 7 and not re.match(r'产品制作时间：\d{8}$', cache[2]):
            return self.sala()
        x = cache[3].split('、')
        for y in x:
            if not re.match(r'[\u4e00-\u9fa5]+\d{8}$', y):
                return self.sala()
        return self.template[2] % tuple(cache)

    def water(self, new_):
        water_1 = '\n'.join(f'{x[0]} {x[1]}' for x in self.water_1.items())
        water_2 = '\n'.join(f'{x[0]} {x[1]}' for x in self.water_2.items())
        info = input(
            f"{' 过滤水 '.center(40, '*')}\n抽样位置：\n{water_1}\n过滤系统信息：\n型号：\n{water_2}\n紫外灯是否开启：\n1 是\n2 "
            f"否\n紫外灯更换日期：\n滤芯更换日期：\n近一周内是否停水停电或故障：\n2 否\n水龙头是否有滤网：\n1 是\n2 否\n水龙头内是否干净无垢：\n1 是\n2 "
            f"否\n最后一次消毒时间（仅限新店）：\n")
        if not info:
            return None
        cache = info.replace(' ', '').replace('，', ',').split(',')
        if not all(cache):
            return self.water(new_)
        if new_ and len(cache) != 9:
            return self.water(new_)
        if not new_ and len(cache) != 8:
            return self.water(new_)
        _ = (cache[3], cache[4], cache[8]) if new_ else (cache[3], cache[4])
        for i in _:
            if not re.match(r'\d{8}$', i):
                return self.water(new_)
        cache[0] = self.water_1.get(cache[0], cache[0])
        cache[1] = self.water_2.get(cache[1], cache[1])
        cache[2] = '开启' if cache[2] == '1' else '关闭'
        cache[5] = '近一周内无停水停电、无故障' if cache[5] == '2' else cache[5]
        cache[6] = '有' if cache[6] == '1' else '无'
        cache[7] = '干净无垢' if cache[7] == '1' else '非干净无垢'
        if new_:
            return self.template[3] % tuple(cache)
        return self.template[4] % tuple(cache)

    def water_(self):
        water__1 = '\n'.join(f'{x[0]} {x[1]}' for x in self.water__1.items())
        info = input(
            f"{' 原水 '.center(40, '*')}\n抽样位置：\n{water__1}\n是否二次供水：\n1 是\n2 否\n")
        if not info:
            return None
        cache = info.replace(' ', '').replace('，', ',').split(',')
        if len(cache) != 2 or not all(cache):
            return self.water_()
        cache[0] = self.water__1.get(cache[0], cache[0])
        cache[1] = '二次供水' if cache[1] == '1' else '非二次供水'
        return self.template[5] % tuple(cache)

    def ice(self):
        ice_1 = '\n'.join(f'{x[0]} {x[1]}' for x in self.ice_1.items())
        ice_2 = '\n'.join(f'{x[0]} {x[1]}' for x in self.ice_2.items())
        info = input(
            f"{' 冰块 '.center(40, '*')}\n抽样位置：\n{ice_1}\n冰铲存放：\n{ice_2}\n制冰机清洗消毒日期：\n")
        if not info:
            return None
        cache = info.replace(' ', '').replace('，', ',').split(',')
        if len(cache) != 3 or not all(
                cache) or not re.match(r'\d{8}$', cache[2]):
            return self.ice()
        cache[0] = self.ice_1.get(cache[0], cache[0])
        cache[1] = self.ice_2.get(cache[1], cache[1])
        return self.template[6] % tuple(cache)

    def drinks(self):
        drinks_1 = '\n'.join(f'{x[0]} {x[1]}' for x in self.drinks_1.items())
        drinks_2 = '\n'.join(f'{x[0]} {x[1]}' for x in self.drinks_2.items())
        drinks_3 = '\n'.join(f'{x[0]} {x[1]}' for x in self.drinks_3.items())
        info = input(
            f"{' 饮料 '.center(40, '*')}\n饮料名称：\n{drinks_1}\n抽样位置：\n{drinks_2}\n产品状态：\n{drinks_3}\n")
        if not info:
            return None
        cache = info.replace(' ', '').replace('，', ',').split(',')
        if len(cache) != 3 or not all(cache):
            return self.drinks()
        cache[0] = self.drinks_1.get(cache[0], cache[0])
        cache[1] = self.drinks_2.get(cache[1], cache[1])
        cache[2] = self.drinks_3.get(cache[2], cache[2])
        return self.template[7] % tuple(cache)

    def tableware(self):
        link_1 = '\n'.join(f'{x[0]} {x[1]}' for x in self.link_1.items())
        tableware_1 = '\n'.join(
            f'{x[0]} {x[1]}' for x in self.tableware_1.items())
        link_3 = '\n'.join(f'{x[0]} {x[1]}' for x in self.link_3.items())
        info = input(
            f"{' 复用餐饮具 '.center(40, '*')}\n抽样位置：\n{link_1}\n器具名称：\n{tableware_1}\n消毒状态：\n{link_3}\n")
        if not info:
            return None
        cache = info.replace(' ', '').replace('，', ',').split(',')
        if len(cache) != 3 or not all(cache):
            return self.tableware()
        cache[0] = self.link_1.get(cache[0], cache[0])
        cache[1] = self.tableware_1.get(cache[1], cache[1])
        cache[2] = self.link_3.get(cache[2], cache[2])
        return self.template[8] % tuple(cache)

    def ion(self, type_):
        ion_1 = '\n'.join(f'{x[0]} {x[1]}' for x in self.ion_1.items())
        info = input(
            f"{f' 阴离子洗涤剂（{type_}）'.center(40, '*')}\n抽样位置：\n{ion_1}\n")
        if not info:
            return None
        if not re.match(r'\d$|[\u4e00-\u9fa5]+$', info):
            return self.ion(type_)
        info = self.ion_1.get(info, info)
        return self.template[9] % info


class KFC(PHDI):
    def __init__(self):
        super().__init__()
        self.template[8] = "抽样位置：%s\n设备型号：%s\n设备最近一次拆机消毒日期：%s\n抽检时%s添加隔夜奶浆\n%s"
        self.link_2 = {
            '1': '不锈钢格',
            '2': '鸡夹',
            '3': '不锈钢勺',
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

    def data(self, new_):
        if not (date := self.date()):
            return None, None
        link = self.link()
        people = self.people()
        sala = self.sala()
        water = self.water(new_)
        water_ = self.water_() if new_ else None
        ice = self.ice()
        drinks = self.drinks()
        milk = self.milk()
        if new_:
            _ = (link, people, sala, water, water_, ice, drinks, milk)
        else:
            _ = (link, people, sala, water, ice, drinks, milk)
        data = []
        for x in _:
            if x:
                data.append(f'"{date}\n{x}"')
            else:
                data.append('""')
        data = '\r\n'.join(data) + '\r\n'
        self.cache_1 = data
        ion = [self.ion(x) for x in self.ion_0]
        return date, ion

    def milk(self):
        milk_1 = '\n'.join(f'{x[0]} {x[1]}' for x in self.milk_1.items())
        milk_2 = '\n'.join(f'{x[0]} {x[1]}' for x in self.milk_2.items())
        info = input(
            f"{' 圣代 '.center(40, '*')}\n抽样位置：\n{milk_1}\n设备型号：\n{milk_2}\n设备最近一次拆机消毒日期：\n抽检时是否已经添加隔夜奶浆：\n1 "
            f"是\n2 否\n近一周内是否停水停电或故障：\n2 否\n")
        if not info:
            return None
        cache = info.replace(' ', '').replace('，', ',').split(',')
        if len(cache) != 5 or not all(
                cache) or not re.match(r'\d{8}$', cache[2]):
            return self.milk()
        cache[0] = self.milk_1.get(cache[0], cache[0])
        cache[1] = self.milk_2.get(cache[1], cache[1])
        cache[3] = "没有" if cache[3] == '2' else "已经"
        cache[4] = '近一周内无停水停电、无故障' if cache[4] == '2' else cache[4]
        return self.template[8] % tuple(cache)


class CJ(PHDI):
    def __init__(self):
        super().__init__()
        self.template[2] = "抽样位置：%s\n产品名称：%s"
        self.template[6] = "制冰机清洗消毒日期：%s\n%s"
        self.link_2[str(len(self.link_2) + 1)] = '打奶钢'
        self.water_2[str(len(self.water_2) + 1)] = '3M'
        self.drinks_1[str(len(self.drinks_1) + 1)] = '冰美式'
        self.drinks_1[str(len(self.drinks_1) + 2)] = '冰拿铁'

    def start(self, new_=False):
        date = self.data(new_)
        if not date:
            return
        while True:
            info = input(f"{'=' * 50}\n下一步：\n1 将样品数据写入剪贴板\n2 返回餐厅选择\n")
            if info == '1':
                pyperclip.copy(self.cache_1)
                print('样品数据已写入剪贴板！')
            elif info == '2':
                break
            else:
                continue

    def data(self, new_):
        date = self.date()
        if date:
            link = self.link()
            people = self.people()
            cake = self.cake()
            water = self.water(new_)
            ice = self.ice()
            drinks = self.drinks()
            tableware = self.tableware()
            _ = (link, people, cake, water, ice, drinks, tableware)
            data = []
            for x in _:
                if x:
                    data.append(f'"{date}\n{x}"')
                else:
                    data.append('""')
            data = '\r\n'.join(data) + '\r\n'
            self.cache_1 = data
        return date

    def cake(self):
        info = input(f"{' 蛋糕 '.center(40, '*')}\n抽样位置：\n产品名称：\n")
        if not info:
            return None
        cache = info.replace(' ', '').replace('，', ',').split(',')
        if len(cache) != 2 or not all(cache):
            return self.cake()
        for i in cache:
            if not re.match(r'[\u4e00-\u9fa5]+$', i):
                return self.cake()
        return self.template[2] % tuple(cache)

    def ice(self):
        ice_2 = '\n'.join(f'{x[0]} {x[1]}' for x in self.ice_2.items())
        info = input(
            f"{' 冰块 '.center(40, '*')}\n制冰机清洗消毒日期：\n冰铲存放：\n{ice_2}\n")
        if not info:
            return None
        cache = info.replace(' ', '').replace('，', ',').split(',')
        if len(cache) != 2 or not all(
                cache) or not re.match(r'\d{8}$', cache[0]):
            return self.ice()
        cache[1] = self.ice_2.get(cache[1], cache[1])
        return self.template[6] % tuple(cache)


def main():
    while True:
        tm = input(
            f"{'=' * 50}\n请选择餐厅类型：\n1 KFC新店\n2 KFC常规\n3 PHDI新店\n4 PHDI常规\n5 C&J\n")
        if tm == '1':
            KFC().start(new_=True)
        elif tm == '2':
            KFC().start()
        elif tm == '3':
            PHDI().start(new_=True)
        elif tm == '4':
            PHDI().start()
        elif tm == '5':
            CJ().start()
        else:
            break


if __name__ == "__main__":
    print(
        f"{' 使用说明 '.center(40, '*')}\n输入序号后按回车键确认\n使用逗号分隔不同的选项（不区分中英文符号）\n没有对应的选项时，可以直接输入内容\n"
        f"不输入内容直接按回车键可以跳过样品\n输入内容错误时会自动提示重新输入")
    main()
