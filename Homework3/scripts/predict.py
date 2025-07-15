import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import os

# 设置中文字体
plt.rcParams['font.family'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False

# 读取清洗后的数据
df = pd.read_csv('D:/test/paper/dataprocess/preprocess/papers_cleaned.csv')
df_counts = df.groupby(['conference', 'year']).size().reset_index(name='count')

# 设置目标会议
conferences = ['AAAI', 'ICML', 'CVPR', 'ICLR', 'IJCAI']

# 创建输出文件夹
os.makedirs("D:/test/paper/output/prediction", exist_ok=True)

# 存储预测结果
prediction_results = []
for conf in conferences:
    df_conf = df_counts[df_counts['conference'].str.upper() == conf.upper()].sort_values('year')
    # 确保有足够数据
    if len(df_conf) < 3:
        print(f"[跳过] {conf} 数据太少，无法预测。")
        continue

    # 训练数据
    X = df_conf['year'].values.reshape(-1, 1)
    y = df_conf['count'].values
    # 模型训练
    model = LinearRegression()
    model.fit(X, y)

    # 动态预测下一年
    last_year = df_conf['year'].max()
    next_year = last_year + 1
    predicted = model.predict(np.array([[next_year]]))[0]

    prediction_results.append({
        'conference': conf,
        'last_year': last_year,
        'predict_year': next_year,
        'predicted_count': int(predicted)
    })

    # 绘图
    plt.figure(figsize=(8, 5))
    plt.plot(X, y, marker='o', label='历史数据', color='#60b8b5')
    plt.plot(next_year, predicted, 'o', color='#ed8585', label=f'{next_year}预测值：{int(predicted)} 篇')
    plt.plot(np.append(X, next_year), model.predict(np.append(X, next_year).reshape(-1, 1)),
             '--', color='#ed8585', label='拟合趋势')

    plt.title(f"{conf} 论文数量预测")
    plt.xlabel("年份")
    plt.ylabel("论文数量")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"D:/test/paper/output/prediction/{conf.lower()}_predict_{next_year}.png")
    plt.close()

# 打印所有预测结果
print("各会议论文数量预测")
for item in prediction_results:
    print(f"{item['conference']}：{item['predict_year']} 年预测值为 {item['predicted_count']} 篇（基于 {item['last_year']} 年）")

# 保存结果
pd.DataFrame(prediction_results).to_csv(
    "D:/test/paper/output/prediction/predicted_paper_counts.csv",
    index=False,
    encoding='utf-8-sig'
)
