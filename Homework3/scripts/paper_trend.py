import os
import pandas as pd
import matplotlib.pyplot as plt

# 设置中文字体
plt.rcParams['font.family'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False

# 确保输出目录存在
os.makedirs("D:/testpaper/output", exist_ok=True)

# 读取数据
df = pd.read_csv('D:/test/paper/dataprocess/preprocess/papers_cleaned.csv')
df_counts = df.groupby(['conference', 'year']).size().reset_index(name='count')

# 绘图
colors = {
    'AAAI': '#FFFB79',
    'ICML': '#A5C947',
    'CVPR': '#5BBFC0',
    'ICLR': '#1E80B8',
    'IJCAI': '#21318C'
}

plt.figure(figsize=(10,6))

for conf in df_counts['conference'].unique():
    subset = df_counts[df_counts['conference'] == conf]
    years = subset['year']
    counts = subset['count']

    plt.plot(years, counts, marker='o', label=conf, color=colors.get(conf, 'black'))
    plt.fill_between(years, counts, color=colors.get(conf, 'black'), alpha=0.2)

plt.title("论文发表数量趋势")
plt.ylabel("论文数量")
plt.xlabel("年份")
plt.legend()
plt.grid(True)

# 保存图像
plt.savefig("D:/test/paper/output/paper_trend.png")
plt.show()
