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

VERSION = 'V0.1.0'

ICO = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\xc8\x00\x00\x00\xc8\x08\x06\x00\x00\x00\xadX\xae\x9e\x00\x00' \
      b'\x00\x01sRGB\x00\xae\xce\x1c\xe9\x00\x00\x10"IDATx^\xed\x9d}\x90\x1bu\x19\xc7\x9fgs\xef}\xbdrPy)/\xe5\xad\xe2' \
      b'\x88\x02\xd5)U\xa0\xd0&P\xda\xcbUG\x8bJ\x13Zu\x1c_yq\x04\xabu,' \
      b'\x0c\x8c\x0e\x8cH\xf1e\x14\x07\x84&=\x10\x19\x85\xe4\x8a\xa5\xc9U\x0f\x95\x17\x19^+\x96B\xb5\x15\n\x85R\xda' \
      b'\xeb\xcb\xf5z\x97K\xf6q6\xa5X\x94\xdb\xddl6\xf7\xfbu\xf7\x9b?{' \
      b'\xbf\xdf\xf3\xf2y\xf6\xd3l\xb2\x9b\x84\t\x0f\x10\x00\x81a\t0\xd8\x80\x00\x08\x0cO\x00\x82\xe0\xe8\x00\x01\x1b' \
      b'\x02\x10\x04\x87\x07\x08@\x10\x1c\x03 \xe0\x8d\x00\x9eA\xbcq\xc3\xae\x90\x10\x80 ' \
      b'!\x194\xda\xf4F\x00\x82x\xe3\x86]!!\x00AB2h\xb4\xe9\x8d\x00\x04\xf1\xc6\r\xbbBB\x00\x82\x84d\xd0h\xd3\x1b\x01' \
      b'\x08\xe2\x8d\x1bv\x85\x84\x00\x04\t\xc9\xa0\xd1\xa67\x02\x10\xc4\x1b7\xec\n\t\x01\x08\x12\x92A\xa3Mo\x04 ' \
      b'\x887n\xd8\x15\x12\x02\x10$$\x83F\x9b\xde\x08@\x10o\xdc\xb0+$\x04 HH\x06\x8d6\xbd\x11\x80 ' \
      b'\xde\xb8aWH\x08@\x90\x90\x0c\x1amz#\x00A\xbcq\xc3\xae\x90\x10\x80 ' \
      b'!\x194\xda\xf4F\x00\x82x\xe3\x86]!!P3A\xe2\xd1{\x8e*\xf1\xd0\x84\xba\x12\xb72S$$<\xd1\xe6\x08\x12(' \
      b'\x11\x0f\xd4IiG\xb1T\xbf\xa3\xab\xe7so\xd5"\xb5o\x82|z\xc6oG\x17\xea\x07?CL\x8b\x88hz-\x8aEL\x10\x18\x96\x80' \
      b'\xd0>!\xfa\x1d\x19\xc6\xaf\xb3\xab?\xd7C\xc4\xe2\x07\xad\xaa\x05\x99{' \
      b'\xc1\xf2\xa3\x8d:c\t\x0b-$\xa6f?\x8aB\x0c\x10\xa8\x86\x80\x88lb\xa2\x9b3\xf9\xe4\xcf\xab\x89c\xed\xf5,' \
      b'H\xfb\x8c\xbb\xdb\xb8\xbex=3\x7f\xb9\xda"\xb0\x1f\x04jA@D^a\xe2\xeb3\xf9\xc4\xed^\xe3{' \
      b'\x12dn\xb4\xf3d\x83J\xdd\xcc|\xac\xd7\xc4\xd8\x07\x02#E@\x88:w\x17\x8eY\xd8\xd3s~\xb1\xd2\x9c\x15\x0b\x12\x8f' \
      b'\xae\xf8\x18\x93<HL\xe3*M\x86\xf5 \xa0\x8a\x80\x88<\xdc8\xd44\xf7\xbe\x9e\xf9}\x95\xd4P\x91 ' \
      b'\xf3b\x9dg\x99Tz\x84\x89\x1b+I\x82\xb5 ' \
      b'\xa0\x07\x01ylWa\xd2\xb9\x95<\x93\xb8\x16\xe4\xe2\x0b:\x8f\xab\x8b\x98O2S\x9b\x1e\xcd\xa2\n\x10\xf0B@\xee\xce' \
      b'\xe4\x92\x97\xba\xdd\xe9Z\x90\x8ehj\x1d1\xbf\xdfm`\xac\x03\x01]\t\x88\xc8\xb7\xb2\xf9\xe4\xcdn\xeas%H\xfb\xac' \
      b'\xd4\x95\x86\xc1\xb7\xb8\tx`\xcd\xe8\xd1\r\xbd\x13\x8f\x1c\xb3\xe5\xb0\xb6\xe6\xde\xba\xbaH\xa9\x92\xbdX\x0b' \
      b'\x02n\x08\x0c\x0c\x14\x1b\xb7m\xdds\xf8\xeb\xaf\xed9\xb6X\x92z7{' \
      b'\xac5B\xd2/\x85\xba\xe3\xdc\\\\t\x14d\xf6\xec\x15c\x1b\x8a\xe6Fb>\xccM\x013/<\x91\xe6\xce\x9bB\'Lnu\xb3\x1ck' \
      b'@\xc0\x17\x02\x8f?\xba\x99\xeeM\xaf\xa5M\x1b{' \
      b']\xc5\x13\x92e\xd9\\\xf2*\xa7\xc5\x8e\x82\xc4c\xe9\xa5Lt\xadS\xa0\xb6\xc3[' \
      b'\xe8;Kg\xd0\x89\'OpZ\x8a\xbf\x83@\xcd\x08\xfc\xfe\xde\x7fP\xea\xd7\xcf\xb8\x8a?T(' \
      b'\x1e\xf9\x87\x9eEo\xd8-v\x16$\x9a~\x89\x99N\xb6\x0b2n|\x13\xdd\xfa\xcb94\xbe\x15\x17\xd2]M\x06\x8bjJ`\xcd\xea' \
      b'\x7f\xd1O\x7f\xfc\x98c\x0e1\xe9\xab\xd9\xee\xc4/<\x0b\x12??}*\xd7\xd3z\xa7L7\xfdd6\x9dr\xaa\xab30\xa7P\xf8' \
      b';\x08\xf8B`\xd9M\x8fP\xcf\x9aM\xb6\xb1\x84\xe8\xa1l.1\xdb\xb3 \x1d\xb1\x15\x8b\x89\xe4\x87v\x01\xa6\x9fs,' \
      b']\xf3\xbds}i\nA@\xc0/\x02om\xeb\xa7/.\xf8\xbdc\xb8}$\xa3s\xb9\xe4\xde\xe1\x16\xda\x9ebuDSw\x12\xf3B\xbb,' \
      b'\x8b\x97\x9eG\xd3\xa6Or,\x04\x0b@`\xa4\t|\xef\xea<=\xbfv\xabmZ&c\xea\x03\xb9K\x9f\xf2$H<\x9a^\xc9Ls\xec2\xfc' \
      b'&\xf3\x19jj\xaa\x1b\xe9\xde\x91\x0f\x04\x1c\t\xdcw\xcf\xf3\xd4y\xd7\xb3\xb6\xebL\xd3\x9c\xd7\xd5}Y\xc6\xab ' \
      b'O0\xd3G\x86\xdb\xdc\xd2ROw\xdf\x7f\x89c\xa1X\x00\x02*\x08<\xfa\x97W\xe8\xa6\x1b\xfel\xff:\xc4\xa4od\xbb\x13' \
      b'?\xf3$HG4\xf5"1\x9f2\xdcf\xeb\xad\xdd\xdbW|RE\xef\xc8\t\x02\x8e\x04\xd6\xaf\xdbF\x8b\xafZm/\x88\xd0\xf5\xd9' \
      b'|\xe2\xfb\x9e\x04\x89\xc7\xd2\x1b\x98\xe8\xa4\xe16\x1f\xd6\xd6BwtB\x10\xc7Ia\x81\x12\x02/\xbe\xf0\x16}\xfb' \
      b'\xca\x87\xecs\x0b\xfd \x93O,\x81 JF\x84\xa4*\t@\x10\x95\xf4\x91[{\x02\x10D\xfb\x11\xa1@\x95\x04 ' \
      b'\x88J\xfa\xc8\xad=\x01\x08\xa2\xfd\x88P\xa0J\x02\x10D%}\xe4\xd6\x9e\x00\x04\xd1~D(' \
      b'P%\x01\x08\xa2\x92>rkO\x00\x82h?"\x14\xa8\x92\x00\x04QI\x1f\xb9\xb5\'\x00A\xb4\x1f\x11\nTI\x00\x82\xa8\xa4' \
      b'\x8f\xdc\xda\x13\x80 \xda\x8f\x08\x05\xaa$\x00AT\xd2Gn\xed\t@\x10\xedG\x84\x02U\x12\x80 *\xe9#\xb7\xf6\x04 ' \
      b'\x88\xf6#B\x81*\t@\x10\x95\xf4\x91[{\x02\x10D\xfb\x11\xa1@\x95\x04 ' \
      b'\x88J\xfa\xc8\xad=\x01\x08\xa2\xfd\x88P\xa0J\x02\x10D%}\xe4\xd6\x9e\x00\x04\xd1~D(' \
      b'P%\x01\x08\xa2\x92>rkO\x00\x82h?"\x14\xa8\x92\x00\x04QI\x1f\xb9\xb5\'\x00A\xb4\x1f\x11\nTI\x00\x82\xa8\xa4' \
      b'\x8f\xdc\xda\x13\x80 \xda\x8f\x08\x05\xaa$\x00AT\xd2Gn\xed\t@\x10\xedG\x84\x02U\x12\x80 *\xe9#\xb7\xf6\x04 ' \
      b'\x88\xf6#B\x81*\t@\x10\x95\xf4\x91[{\x02\x10D\xfb\x11\xa1@\x95\x04 ' \
      b'\x88J\xfa\xc8\xad=\x01\x08\xa2\xfd\x88P\xa0J\x02\x10D%}\xe4\xd6\x9e\x00\x04\xd1~D(' \
      b'P%\x01\x08\xa2\x92>rkO\x00\x82h?"\x14\xa8\x92\x00\x04QI\x1f\xb9\xb5\'\x00A\xb4\x1f\x11\nTI\x00\x82\xa8\xa4' \
      b'\x8f\xdc\xda\x13\x80 \xda\x8f\x08\x05\xaa$\x00AT\xd2Gn\xed\t@\x10\xedG\x84\x02U\x12\x80 *\xe9#\xb7\xf6\x04 ' \
      b'\x88\xf6#B\x81*\t@\x10\x95\xf4\x91[{\x02\x10D\xfb\x11\xa1@\x95\x04 ' \
      b'\x88J\xfa\xc8\xad=\x01\x08\xa2\xfd\x88P\xa0J\x02\x10D%}\xe4\xd6\x9e\x00\x04\xd1~D(' \
      b'P%\x01\x08\xa2\x92>rkO\x00\x82h?"\x14\xa8\x92\x00\x04QI\x1f\xb9\xb5\'\x00A\xb4\x1f\x11\nTI\x00\x82\xa8\xa4' \
      b'\x8f\xdc\xda\x13\x80 \xda\x8f\x08\x05\xaa$\x00AT\xd2Gn\xed\t@\x10\xedG\x84\x02U\x12\x80 *\xe9#\xb7\xf6\x04 ' \
      b'\x88\xf6#B\x81*\t@\x10\x95\xf4\x91[{\x02\x10D\xfb\x11\xa1@\x95\x04 ' \
      b'\x88J\xfa\xc8\xad=\x01\x08\xa2\xfd\x88P\xa0J\x02\x10D%}\xe4\xd6\x9e\x00\x04\xd1~D(P%\x01\x08\xa2\x92>rkO@\xb9 ' \
      b'\xe3\xc65\xd1\xd5K\xce\xd1\x1e\x14\n\x0c\'\x81\xcd\xaf\xec\xa2\xdb~\xf6\xc4{' \
      b'4\xcfD$\xfb\xff]\xe8\x07\x99|b\xc9p\x84\xac\x95\xc3>\xe2\xb1\xf4\x06&:)\x9cx\xd1up\t\x08\x910\xd1~O\xaa\x11$' \
      b'\xf5O&>1\xb8\xa0\xd0Y\x98\t\x88\x081\xb1wA:b\xa9\xedD<!\xcc\x10\xd1{' \
      b'\xc0\t\x88\xfc2\x93O~\xc5\xdb)V4\xdd\xcfL\xcd\x01G\x84\xf6BL@\x84Ve\xf3\x89\x8b=\t\xd2\x1eM\xed3\x98\x9bB\xcc' \
      b'\x0f\xad\x07\x9c\x80)\x94\xeb\xca\'.\xf4$HG4\xd5K\xcc\xe3\x03\xce\x08\xed\x85\x98\x80\x08-\xcf\xe6\x13\x0b=\t' \
      b'\x12\x8f\xa572\xd1\t!\xe6\x87\xd6\x83N\xa0\xbaw\xb1\xd2\x1b\x88\xe8$.\xbfgl\xfb\x8ep\xd01\xa2\xbf\x80\x11' \
      b'\x10y\xe7\x88\xf6\xfe.\xd6\xbb\xae\x83\xbc\xed\xc8\xdb\x97W\xca\xb8"\x11\xa6\xa3\'\x8d\r\x18:\xb4\x13\x14\x02' \
      b'\x83\x83E\xda\xfa\xfa\xdew\xb5\xc3\xd6\x7f\xf4\x07\xd9Q\xe5u\x10\xfb\x0b\x85\r\x8d\x11\xfa\xe8\xf4\xa3\x83' \
      b'\xc2\x13}\x04\x8c\xc0\xee]\x83\xb4\xf6\xe9\xad\xf6]U{\x8aew%\x1d\x82\x04\xec\x88\nX;\x10$`\x03E;\xfe\x12\x80 ' \
      b'\xfe\xf2D\xb4\x80\x11\x80 \x01\x1b(\xda\xf1\x97@\xed\x05\x89\xa6\x9ef\xe63\x86+\xbb.\xc24\xed\xdcI\xfev\x85h ' \
      b'\xe0\x13\x81\xde\x1d\xfb\xe8\x1f\xcfmsz\x91\xbe8\x93O\xdc8\xdc"\x87\xdb\xddS]L<\xd7.\xc3\xf4\xf3&\x91a\xe0' \
      b'\x1a\x89O3E\x18\x1f\tXo\xf1nX\xbf\xdd6\xa2\x10-\xc8\xe6\x12\x9d\xde\x04\x89\xa6ng\xe6/\xd8e\xf8\xc0\x87\x0e' \
      b'\xa7\xd6\t\xb8\x9f\xd1\xc7\xb9"\x94O\x04^za;\xbd\xf9\xc6\xbb\xaf\x83\xfco\xe8\x92\xf0\xac\x95\xf9\x05k<\t' \
      b'\xd21+\xb5\x84\x0c\xbe\xc1\xae\xde\xf7\x1d5\x9aN:\x15w\xc4\xfb4S\x84\xf1\x89\x80i\n=\xf1\xc8\xabT,' \
      b'\x1e|i\xfb\xff\x83\x9b$\x93\xbbr\xc9M\x9e\x04\x99\x17\xeb<K\xc8|\xd2\xaeff\xa2\xa9\xd3\x8e\xa2\xc6\xa6:\x9fZC' \
      b'\x18\x10\xa8\x9e\xc0\xe6\x97w\xd3\xcb\x1bw\xda\x9f^\tm\xc8\xe6\x13\xa7\xd8\x1e\xdfN\xa5t\xc4\xd2[' \
      b'\x88\xe8H\xbbuc\xc66\xd0\x07\xcf\x98\x88\xd7"N0\xf1\xf7\x11!\xd0\xb7\xa7P\xbe\x82n=\x8b\xd8=D\xe4\x87\xd9' \
      b'|\xf2\xbbU\t\x12\x8f\xa6\x971\xd3\x15N\x9d\xb5Nh\xa2)\x1fh\xa3H\x9d\xe1\xb4\x14\x7f\x07\x81\x9a\x11\xb0\xde' \
      b'\xda]\xf7\xf7mT\x1c2\x1ds\x88i\x9e\x99\xed\xbe\xec\x99\xaa\x04\x99;k\xf9\xb1\x11\xc3x\xd91\x1bQ\xf94\xeb\xf8' \
      b'\xc9\xe3\xe8\xf0\x89\xa3\xdc,\xc7\x1a\x10\xf0\x8d\xc0P\xa1D\xd6i\xd5\x96W\xf7\xb8\x8b)\xb2:\x93O^\xe4\xb4\xd8' \
      b'\xd5\xfb\xb3\xf1h\xfaff\xfa\xa6S\xb0\x03\x7f\xaf\xaf7\xa8\xed\x88\x16\x1a5\xaa\x81\x9aZ\xea\xac\x0f\xc6\xbb' \
      b'\xdd\x1a\xb8u}}\x85\xf2\xa9gSs\x9do\xa7\xa0CC%*\x0c\x96(' \
      b'b\x18\xe5\xb8a}\x94J&\xf5\xf7\x17i\xe7\x8e~\xda\xd9;X\x11\x86\x12\xd3\x87W\xaeN<\xe7\xb4\xc9\xd5\x91;\xe7\xe3' \
      b'\x9d\xadu\xcd\xa5\x8d\xf8t\xa1\x13N\xeb\xef\x07}\xa5\x8c\x9b\xe5\xbe\xae90N\xfbso_S\x1e\x8a\xc1D\xee\xca\xe4' \
      b'\x93\x8b\xdc\x94\xeeJ\x10+P<\xd6y.\x93\xf9G\xebc ' \
      b'n\x02\x87k\x8d\x85\xd1:\xe7u\x8d3\\x4\xeaVH\xd6Jc\xeb\xd9]]\xed\xfdn\xca\xaah\xa2\xf1\xd8\x8a\xcf3\xc9\x1dn' \
      b'\x02\x87g\x8d\xc6\x9f\xb6,\x7f0\xa8\xa2\x11\x07zl"\xb4uh\x88\xa7\xae\xeaY\xf0\xaa\xdbF+\xa6\x17\x8f\xa6\xaea' \
      b'\xe6a\xef]q\x9b\x18\xebF\x88\x00$)\x83\x16\xa1-%\x96\x0b\x1f\xcc%\x9f\xaf\x84|\xc5\x82X\xc1;b+>Eb\xdeM\xcc' \
      b'\xf5\x95$\x0b\xcc\xdaC\xed\xa0\x13!\xe1\x10\xbfU"\xb4\xce`9\xff\xfe\\\xf2\xcdJ\x8fAO\x82\x94%\x99\x99>G"\xf2' \
      b'+&\x9eRi\xd2Cz\xfd\xa1&\xc7A\xb05>\x19\xac\xd9!!D\xcb\x1b\x0b\x8d_\xbf\xafg~\x9f\x97$\x9e\x05\xd9\x9f\xecZ' \
      b'#\x1e\x9b<\x9f\x88\x96\x86A\x94C\xd8\x8d\xfd\xe3:\xe4\x1bp{' \
      b'\x88\x8b)\xc4\xf7\x10\xd3\xb5\xd9\xd5\x89\x7f\xba\xdd\xf5^\xeb\xaa\x14\xe4\xbf!\xe7\xce\\~\xb6ap;\x13w\x10' \
      b'\xd3i\xd5\x14\x85\xbd\xb5$\x10\xdc\xe7\x11\x11y\x85\x89\xee \xae\xbf3\x93\xfb\xecf?(' \
      b'\xfa&\xc8\xc1\xc5\xcc\x9e\xbdbl\xc4\xe4)\x86\x94&S\xf9\x8b\xe7\xb8\xd1\x8fbU\xc6`\x91+*\xba\x0e\x141\xc8h' \
      b'\x1dE<\xa6\x85\xd8`\xe2\xd1Md\xb4U\xff\x15I20Dfo\x1f\xc9@\x81\xa4P"\xd9\xd9G\xd27P\x11\x1aS\xe8af\xea\xa9h' \
      b'\x93\x86\x8b\x99x@Ls\xbb\x10\xef \xe2\xd7\xba\xba\x17<\xeew\x995\x11\xc4\xef"U\xc7k\x8f\xa6\x16\x1a\xccw\xba' \
      b'\xa9\xc3\x18?\x8a\x1a\xa3\xa7S\xe3Y#\xf7\xab\x11\xb2\xaf@\x03\x7f]O\x83k\xd6\xba)\xd1:\xd5\xda\xc9C\xa5\x13' \
      b'\x1e\xe8Yd\x7f\xbb\xab\xbbh\x81^\x05A\\\x8c\xb7#\x96\xdaD\xc4\xc7;-\xad?s2\xb5\xb4O%nnpZZ\x93\xbf\x97\xb6\xf4' \
      b'\xd2\xdeT\x0f\x99;\xed?$T~9Bt]6\x97\xb8\xb6&\x85\x04((' \
      b'\x04q\x18\xe6\xbch\xe7\x87\x85M\xdb;>\xad\x10\x96\x1c\xa3\xe6OW~h\x98\xbd{' \
      b'i\xcf\xb2\x95$\x83C\x0e\xb5\xc8\xbf3\xb9$\xbew\xd9\x81\x12\x04q\x00\xe4\xe6v\x7f\xeb\xb4j\xcc\x15s\x94=s\xfco' \
      b'\x0b\xc5\x8d[\xa9\xefWyGYY\x8c3\x1e\xc8_\xfa\xac\xe3\xc2\x10/\x80 ' \
      b'\x0e\xc3wsz\xd5\xfc\xe9\xb3G\xf45\x87\x9b\xe3u\xcfm9*m\xb2\xbf.f\x9arUWwr\x99\x9bxa]\x03A\x1c\x05I\xdb\xde' \
      b'\x1a\xcb\x8d\xf54\xee\xbaK\xb4;~\n\xeb6S\x7f\xeaa\xdb\xba\xac\x8bh\xd9\xdc\xf0\xbf\x8d\xa1]S\n\n\x82 ' \
      b'U\nRw\xda14:9C\xc1\xe8\x9cS\xee\\\xbc\xc2^\x10\x91\x87\xb3yM\x8bwnoDV@\x10\x1b\xcc\xf3f\xa5g\x88A\x7f\xb2' \
      b'\x9bD\xe3\xcc\xd3\xa99z\xfa\x88\x0c\xab\xd2$\xbb\x96\xdek\xffb]\xe8\xd9L>1\xec\x17\x03V\x9a/\x88\xeb!H\x80' \
      b'\x05q\xf3:$\x93K\xe0\x18\xb09\x06\x00\'\xc8\x82\xdc\xfa ' \
      b'\x95^\xef\x1d\xbeC\xa1]\x99|\x02\xbfA\tA\xbc=\xf9\xbb\xb9\x06\xd20}\n\xb5\xc4\xa7zKP\xe3]x\rR=`<\x83T\xf9' \
      b'"=rdk\xf9\x1a\x88n\x0f\xeb\x82\xe1\xee\x1b\xef\xc7\x8b\xf4*\x07\x03A\xaa\x14\xc4\xda>\xf6\xdb\x9f(' \
      b'\xdf\x98\xa8\xd3c\xe0\xaf/\xd0\xc0\xca\xa7\x1c\x04\xa1[\xb3\xf9\xc4\x95:\xd5\xad[' \
      b'-\x10\xc4a"\xf1X\xea\x81\xf2-\xfc6\x0f\x1dO\xb3\xacg\x0f\xebY\xc4\xeea\x8a,' \
      b'\xea\xca\'\xef\xd2\xed\xa0\xd4\xa9\x1e\x08\xe20\r\xb7w\xf2\x8e\xb9|\x0eE\x8ej\xd5b\xb6\xfd\xd9\'\xa9\xf0\xe8z' \
      b'\xc7Z\xb8Pl\xc5\x1d\xbd\xf6\x98 \x88\xc3a4\xef\xa2{' \
      b'\x8e\x17\xb38\xec\xb7\x7f\x1f\xd8\xceM\xf54\xfaK1\xe5\x92\x0c>\xf5/\xdaw\xdfc\x8er\x08I&\x9bK\xces\\\x18\xf2' \
      b'\x05\x10\xc4\xc5\x01\x10\x8f\xa6z\x98\xf9<\xa7\xa5\x96$\xcd\xf3\xa7S\xc3i#\xff\xab[' \
      b'\xe5\xcf\x84t\xaf\xa5\xc1G\x9c\x9f9\xac>pz\xe54\xcd\xfd\x7f\x87 ' \
      b'.8\xb9}\x169\x10\xaan\xf2Dj\x98z"\xd5\xbf\xff\x98\x9a\xdf\xe1k}\x06\xa4\xb8i+\r\xe4\x9f#\xeb\xd3\x86n\x1e' \
      b'\x82[L\xdc`\n\x9e \xf1\x0b;\xcf\'1\x7fD"\xa71s\x93k\nXX=\x01\x917\x85\xf8\xf1A\xa3q\xd1\xea\xd5\xf3wT\x1fP' \
      b'\x8f\x08\x81y\x06\x89\xcfL_\xc4\x11Z\xa5\x07\xd6\xf0V!D/\x1a\x85\xe2\xb4\xa0\xbc\xf8\x0f\x84 ' \
      b'\xd6\x97D4\x14\xcd\r\xc4|Dx\x0fM\x8d:\xaf\xe0\xcb\xa15\xaa\xfa=K\t\x84 ' \
      b'\xed\xb1\xd4\x97\x0c\xe2\xdbt\x87\x1d\xa6\xfa\n\x11\x1e\xb7j\xd5\x82\xdd\x87z\xcf\x81\x10$\x1eK\xdd\xc2\xc4' \
      b'\xb8"\xac\xd5\xd1(\xd32\xb9\xe4\xdf\xb4*\xc9C1\x81\x10\xa4#\x96\xba\x9c\x88o\xf5\xd0?\xb6\xd4\x88\xc0^\xb3q|w' \
      b'\xf7\xfc]5\n?ba\x03!H{,u\x02\x0b\xfd\x9d\x99\xf5\xba!j\xc4\xc6\xa8W"!\xcags\x89\x98^Uy\xab&\x10\x82X\xadwDS' \
      b'\x17\x0b\xd1o!\x89\xb7\x03\xc1\xaf]\xd6\x0f\xd4DJr\xc1\xfdk.\xdb\xeeWL\x95q\x02#\x88\x05q\xce\xcc\xce\xc9\x11' \
      b'\xc3\xfcZ\xf9\xbb\x81E\x9a\x15\x81m"\x916f\xb6~<p\xdc;50\xf7\x89\xc8kDT\xd9\xf7\x84\xfe\x7f\x13mD<\x91I\xca' \
      b'?N(L\x03,4(D\xd6\xb7\x97\xbf\xa5\xa8g\xeb\x9a\xf3V&z:\x93O\x04\xea\xb7c\x02%\x88\xba\x83\x03\x99\x83J\x00\x82' \
      b'\x04u\xb2\xe8\xcb\x17\x02\x10\xc4\x17\x8c\x08\x12T\x02\x10$\xa8\x93E_\xbe\x10\x80 \xbe`D\x90\xa0\x12\x80 ' \
      b'A\x9d,\xfa\xf2\x85\x00\x04\xf1\x05#\x82\x04\x95\x00\x04\t\xead\xd1\x97/\x04 \x88/\x18\x11$\xa8\x04 ' \
      b'HP\'\x8b\xbe|!\x00A|\xc1\x88 A%\x00A\x82:Y\xf4\xe5\x0b\x01\x08\xe2\x0bF\x04\t*\x01\x08\x12\xd4\xc9\xa2/_\x08' \
      b'@\x10_0"HP\t@\x90\xa0N\x16}\xf9B\x00\x82\xf8\x82\x11A\x82J\x00\x82\x04u\xb2\xe8\xcb\x17\x02\x10\xc4\x17\x8c' \
      b'\x08\x12T\x02\x10$\xa8\x93E_\xbe\x10\x80 \xbe`D\x90\xa0\x12\x80 A\x9d,' \
      b'\xfa\xf2\x85\x00\x04\xf1\x05#\x82\x04\x95\x00\x04\t\xead\xd1\x97/\x04\xfe\x03\x13\xd8q2\x1e\x92rk\x00\x00\x00' \
      b'\x00IEND\xaeB`\x82 '


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
        f'报告编辑部小工具 {VERSION}',
        layout,
        size=(
            405,
            195),
        text_justification='center',
        element_justification='center',
        icon=ICO,
        finalize=True, )


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
        icon=ICO,
        finalize=True,
        return_keyboard_events=True)


def nutrition(window):
    window_item = nutrition_win()
    window.Hide()
    while True:
        event_n, values_n = window_item.read(timeout=100)
        if event_n == '-WINDOW CLOSE ATTEMPTED-':
            window_item.close()
            window.UnHide()
            return window
        elif event_n in ['计算', '\r']:
            try:
                del values_n['status']
                numbers = [decimal.Decimal(i) for i in values_n.values()]
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
                data = data[:-1]
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
        icon=ICO,
        finalize=True,
        return_keyboard_events=True)


def nutrition_plus(window):
    window_item = nutrition_plus_win()
    window.Hide()
    while True:
        event_np, values_np = window_item.read(timeout=100)
        if event_np == '-WINDOW CLOSE ATTEMPTED-':
            window_item.close()
            window.UnHide()
            return window
        elif event_np in ['计算', '\r']:
            try:
                del values_np['status']
                numbers = [decimal.Decimal(i) for i in values_np.values()]
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
                data = data[:-1]
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
        icon=ICO,
        finalize=True,
        return_keyboard_events=True)


def dehydration(window):
    window_item = dehydration_win()
    window.Hide()
    remark = None
    while True:
        event_d, values_d = window_item.read(timeout=100)
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
        [sg.Button('微生物备注', key='00', font=('微软雅黑', 10))],
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
        icon=ICO,
        finalize=True)


def clipboard(window):
    window_item = clipboard_win()
    window.Hide()
    while True:
        event_d, values_d = window_item.read(timeout=100)
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
        icon=ICO,
        finalize=True,
        return_keyboard_events=True)


def solid_drink(window):
    window_item = solid_drink_win()
    window.Hide()
    remark = None
    while True:
        event_s, values_s = window_item.read(timeout=100)
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
    sg.theme_add_new('RE_Theme', theme)
    sg.theme('RE_Theme')
    window = home()
    while True:
        event, values = window.read(timeout=100)
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
    window.close()


if __name__ == '__main__':
    main()
