from wordcloud import WordCloud
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import random

# 设置中文字体
plt.rcParams['font.family'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False

# 读取数据
df = pd.read_csv('D:/test/paper/dataprocess/preprocess/papers_cleaned.csv')
titles = df['title'].dropna().values.astype('U')

# 提取词频
vectorizer = CountVectorizer(stop_words='english', max_features=100)
X = vectorizer.fit_transform(titles)
word_freq = dict(zip(vectorizer.get_feature_names_out(), X.sum(axis=0).tolist()[0]))

# 自定义配色
hex_colors = [
    "#19dfd5", "#72b4eb", "#f7f50c", "#6177f7", "#81bcf7",
    "#9cef5d", "#bdef33", "#85e8f7", "#1dbd97", "#2ba43a"
]

# 定义随机颜色函数
def random_color_func(word, font_size, position, orientation, font_path, random_state):
    return random.choice(hex_colors)

# 生成词云
wordcloud = WordCloud(
    width=1000,
    height=600,
    background_color='white',
    color_func=random_color_func
).generate_from_frequencies(word_freq)

# 显示与保存
plt.figure(figsize=(12, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.title("研究热点关键词词云（2020-2025）", fontsize = 16)
plt.savefig("D:/test/paper/output/wordcloud_keywords.png")
plt.show()
