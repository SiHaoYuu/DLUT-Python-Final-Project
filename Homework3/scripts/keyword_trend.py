import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer

# 设置中文字体
plt.rcParams['font.family'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False

# 读取论文数据
df = pd.read_csv('D:/test/paper/dataprocess/preprocess/papers_cleaned.csv')
df = df[['title', 'year']].dropna()
df['title'] = df['title'].astype(str).str.lower()

# 设置追踪关键词
keywords_to_track = ['learning', 'neural', 'image', 'language', '3d', 'networks', 'multimodal']

# 手动设置颜色
colors = {
    'learning': '#93c5dd',
    'neural': '#83d8cf',
    'image': '#fae1a4',
    'language': '#f1a7b8',
    '3d': '#c65c7a',
    'networks': '#a57eb6',
    'multimodal': '#2380b9'
}

# 统计关键词频次按年份
year_list = sorted(df['year'].unique())
keyword_freq_by_year = {kw: [] for kw in keywords_to_track}

for year in year_list:
    titles = df[df['year'] == year]['title'].tolist()
    joined_text = ' '.join(titles)
    vectorizer = CountVectorizer(vocabulary=keywords_to_track)
    X = vectorizer.fit_transform([joined_text])
    freqs = X.toarray().flatten()
    for i, kw in enumerate(keywords_to_track):
        keyword_freq_by_year[kw].append(freqs[i])

# 绘图
plt.figure(figsize=(12, 6))
for kw in keywords_to_track:
    plt.plot(year_list,
             keyword_freq_by_year[kw],
             marker='o',
             label=kw,
             color=colors.get(kw, 'black'),
             linewidth=2.5)  # 指定颜色

plt.title("研究热点关键词随年份变化趋势", fontsize=16)
plt.xlabel("年份", fontsize=12)
plt.ylabel("关键词出现频次", fontsize=12)
plt.legend()
plt.grid(True)
plt.tight_layout()

# 保存图像
plt.savefig("D:/test/paper/output/keyword_trend_colored.png")
plt.show()
