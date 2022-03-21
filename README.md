# 办公小工具

~~使用 Python 编写各种提高效率的小工具，代码可供学习和使用。~~

**2022/3/21：该项目不再更新！**

*****

## 报告编辑部小工具（专用）

<details>
    <summary>安装依赖</summary>

* pip install pysimplegui

</details>

<details>
    <summary>功能说明</summary>

### 营养成分表计算

* 数值修约规则为四舍六入五成双。
* NRV% 均使用修约数值进行计算。
* NRV% 计算结果数值在 0.5%~1.0% 之间时均修约为1%。
* 从 Word 文档复制五项营养成分数值（包括单位），点击按钮可自动导入并填充数值。
* 输入数值点击计算，程序会根据“蛋白质”、“脂肪”、“碳水化合物”的修约数值计算得出能量数值，计算公式为：能量=蛋白质×17+脂肪×37+碳水化合物×17。并将能量的计算数值与输入数值进行对比，检查两者数值之差是否超过
  20.0，若相差不大于 20.0，以绿色文本展示计算结果；反之以红色文本展示计算结果。
* 能量计算结果分别为：原始计算数值，修约计算数值，NRV% 原始百分比，NRV% 修约百分比。

### 脱水率限值计算

* 数值修约规则为四舍六入五成双。
* 点击常见样品按钮可自动填充部分数值。
* 已知脱水率时，鲜品水分输入100，本品水分输入脱水率数值即可。
* 脱水率计算公式：（鲜品水分-本品水分）÷（1-本品水分）
* 限值折算公式：项目限值÷（1-脱水率）
* 点击计算后，再次点击复制备注按钮可智能复制相对应的备注内容至剪贴板。

### 固体饮料限值计算

* 数值修约规则为四舍六入五成双。
* 限值折算结果最多保留四位小数。
* 点击常见固体饮料按钮可自动填充部分数值。
* 固体饮料限值折算公式：（（样品量+水）÷样品量）×项目限值
* 点击计算后，再次点击复制备注可智能复制相对应的备注内容至剪贴板。

### 常用内容剪贴板

* 点击按钮即可复制相对应的无格式文本至剪贴板。

</details>

## 印章检测小工具（专用）

<details>
    <summary>安装依赖</summary>

* pip install fitz
* pip install PyMuPDF
* pip install opencv-python
* pip install pysimplegui
* pip install openpyxl

</details>

<details>
    <summary>使用说明</summary>

**检测扫描件（PDF 格式）中每页是否存在红色圆形印章。**

程序检测完成后会在 PDF 文件所在文件夹生成同名 xlsx 文件，该文件包含检测结果；另外还会在程序所在文件夹生成检测记录文件。

程序默认仅保存异常结果，当生成的 xlsx 文件名称以 “ _正常 ” 结尾时说明该 PDF 文件均为正常页；当选择保存全部结果时，文件检测结果不会在 xlsx 文件名体现，需要打开 xlsx 文件查看完整检测结果。

低性能模式：减少程序检测文件时占用的内存，但是会增加检测文件所用的时间，建议低配置电脑或处理大文件时启用。

| 状态    | 含义              |
|-------|-----------------|
| True  | 正常页，检测到印章       |
| False | 异常页，未检测到印章      |
| None  | 未知页，红色区域过大，跳过检测 |

</details>

<details>
    <summary>实现原理</summary>

1. 将 PDF 文件中的每页转换成图像
2. 将每页的图像从 BGR 颜色空间转换成 HSV 颜色空间
3. 在 HSV 颜色空间下提取图像的红色部分
4. 对提取到的红色部分进行膨胀形态学操作
5. 将膨胀后的图像转换成灰度图
6. 使用霍夫圆变换在灰度图中检测圆

</details>

## 异常页面检查辅助工具（专用）

<details>
    <summary>安装依赖</summary>

* pip install fitz
* pip install PyMuPDF
* pip install pysimplegui
* pip install pandas
* pip install openpyxl

</details>

<details>
    <summary>使用说明</summary>

**本程序需要配合“印章检测小工具”使用，且“印章检测小工具”版本要求≥0.1.1。**

程序启动时会自动扫描当前目录，读取检测记录文件获取 PDF 文件检测记录，需要将本程序与“印章检测小工具”放置于同一文件夹内（非必需）

在程序主界面点击选中需要检查的文件，然后点击“检查文件”按钮开始预览检查；或者点击“浏览文件”选择 XLSX 格式的检测结果文件，如果选择的文件含有非正常页，程序会自动开始预览检查。

低性能模式：减少程序处理文件时占用的内存，但是会增加处理文件所用的时间，建议低配置电脑或处理大文件时启用。

</details>

## 数据录入小工具（专用）

数据录入辅助工具，详细使用方法可在程序内查阅。
