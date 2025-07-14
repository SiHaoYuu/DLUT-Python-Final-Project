# 注意！

1. 作者力推使用```Homework4.ipynb```这个Jupyter Notebook文件进行数据分析和可视化，以及对作业的查验。你可以选择使用以下代码在终端安装并使用Jupyter：
```bash
pip install jupyter
jupyter notebook
```
或者采用```Visual Studio Code```（简称```VSCode```）里面的Jupyter插件和其他便于可视化的插件以实现更好的交互体验

2. 如果你实在不想折腾，那么你可以打开```./Code/Homework4.py```，在终端使用以下语句运行代码：
```bash
python ./Code/Homework4.py
```
生成的可视化图片和数据与使用Jupyter Notebook一致，不太一样的地方在于.py不会有交互式的图片和数据窗口生成。

3. 文件夹下有两个.csv文件，```大乐透100期数据.csv```采用UTF-8编码，是使用vscode插件可以阅读的，可以使用下面代码读取到Python文件中
```python
import pandas as pd
pd.DataFrame = pd.read_csv('大乐透100期数据.csv')
```
而```大乐透100期数据excel版.csv```采用ANSI默认字符集（中文是GBK），是可以在Excel中打开不乱码的，减少了没有必要插件还读取不到有效数据的苦恼。