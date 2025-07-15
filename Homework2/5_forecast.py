import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error
import os

# 设置中文字体支持
plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题

# 优化图表基础样式
plt.rcParams["figure.dpi"] = 300  # 高分辨率
plt.rcParams["axes.grid"] = True  # 网格线
plt.rcParams["grid.alpha"] = 0.2  # 网格透明度
plt.rcParams["axes.spines.top"] = False  # 隐藏上边框
plt.rcParams["axes.spines.right"] = False  # 隐藏右边框
plt.rcParams["lines.linewidth"] = 2  # 线条宽度
plt.rcParams["lines.markersize"] = 6  # 标记大小
plt.rcParams["legend.fontsize"] = 12  # 图例字体
plt.rcParams["xtick.labelsize"] = 10  # x轴标签字体
plt.rcParams["ytick.labelsize"] = 11  # y轴标签字体


def process_data(df):
    """数据预处理，提取年份、月份并计算每月平均气温"""
    df['date'] = pd.to_datetime(df['date'], format='%Y年%m月%d日')
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    return df


def train_arima(time_series):
    """训练ARIMA模型，优先尝试季节性模型"""
    try:
        # 季节性ARIMA
        model = ARIMA(time_series, order=(2, 1, 1), seasonal_order=(1, 1, 1, 12))
        model_fit = model.fit()
        return model_fit
    except Exception as e:
        print(f"季节性ARIMA失败，改用简单模型: {e}")
        # 简单ARIMA
        model = ARIMA(time_series, order=(2, 1, 0))
        model_fit = model.fit()
        return model_fit


def plot_temperature_trend(data_path=r"E:\Users\lzr20\PycharmProjects\pythonProject2\weather_data\dalian_weather_data.csv"):
    """绘制整合后的温度趋势对比图"""
    # 数据读取
    if not os.path.exists(data_path):
        print(f"错误: 数据文件 '{data_path}' 不存在")
        return

    try:
        df = pd.read_csv(data_path)
        print(f"成功读取 {len(df)} 条数据")
    except Exception as e:
        print(f"数据读取失败: {e}")
        return

    # 数据预处理
    df = process_data(df)

    # 历史数据（2022-2024年）
    train_years = [2022, 2023, 2024]
    train_df = df[df['year'].isin(train_years)]
    if train_df.empty:
        print("错误: 无2022-2024年有效数据")
        return

    # 计算每月平均最高气温（历史数据）
    monthly_avg = train_df.groupby(['year', 'month'])['max_temperature'].mean().reset_index()
    monthly_avg.columns = ['年份', '月份', '平均最高气温']

    # ARIMA模型训练与预测（2025年1-6月）
    time_series = monthly_avg['平均最高气温']
    model_fit = train_arima(time_series)
    forecast = model_fit.forecast(steps=6)
    forecast_df = pd.DataFrame({
        '年份': [2025] * 6,
        '月份': range(1, 7),
        '预测平均最高气温': forecast
    })

    # 实际数据（2025年1-6月）
    actual_2025 = df[(df['year'] == 2025) & (df['month'] <= 6)]
    has_actual = not actual_2025.empty
    if has_actual:
        actual_avg = actual_2025.groupby('month')['max_temperature'].mean().reset_index()
        actual_avg.columns = ['月份', '实际平均最高气温']

    # 构建绘图数据：按月份整理各年份数据
    months = range(1, 13)  # 完整12个月
    years = [2022, 2023, 2024, 2025]

    # 历史数据（2022-2024）
    history_data = {}
    for y in years[:-1]:
        year_data = monthly_avg[monthly_avg['年份'] == y]
        history_data[y] = [year_data[year_data['月份'] == m]['平均最高气温'].values[0]
                           if len(year_data[year_data['月份'] == m]) > 0 else np.nan
                           for m in months]

    # 预测数据（2025）
    forecast_data = [forecast_df[forecast_df['月份'] == m]['预测平均最高气温'].values[0]
                     if len(forecast_df[forecast_df['月份'] == m]) > 0 else np.nan
                     for m in months]

    # 实际数据（2025）
    actual_data = [actual_avg[actual_avg['月份'] == m]['实际平均最高气温'].values[0]
                   if has_actual and len(actual_avg[actual_avg['月份'] == m]) > 0 else np.nan
                   for m in months]

    # 绘图：多曲线对比
    plt.figure(figsize=(14, 8))  # 舒展的画布尺寸

    # 绘制历史年份曲线（2022-2024）
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    for i, y in enumerate(years[:-1]):
        plt.plot(months, history_data[y], marker='o', label=f'{y}年', color=colors[i])

    # 绘制2025年预测与实际曲线
    plt.plot(months, forecast_data, marker='s', label='2025年预测', color='#d62728', linestyle='--')
    if has_actual:
        plt.plot(months, actual_data, marker='^', label='2025年实际', color='#9467bd', linestyle='--')

    # 坐标轴优化
    plt.xticks(months, [f'{m}月' for m in months], rotation=0)  # 月份横向显示
    plt.xlabel('月份', fontsize=14, labelpad=15)
    plt.ylabel('平均最高气温 (°C)', fontsize=14, labelpad=15)

    # 标题与图例
    plt.title('2022-2025年大连市每月平均最高气温变化趋势', fontsize=18, pad=20)
    plt.legend(loc='upper left', bbox_to_anchor=(0.02, 0.85), ncol=2)  # 分两列显示图例

    # 误差标注（如果有实际数据）
    if has_actual:
        mae = mean_absolute_error(actual_data[:6], forecast_data[:6])
        rmse = np.sqrt(mean_squared_error(actual_data[:6], forecast_data[:6]))
        plt.text(0.02, 0.90, f'MAE: {mae:.2f}°C  |  RMSE: {rmse:.2f}°C',
                 transform=plt.gca().transAxes, fontsize=12, color='darkred')

    # 布局调整
    plt.subplots_adjust(left=0.1, right=0.95, top=0.85, bottom=0.15)

    # 保存与显示
    output_dir = 'weather_plots/forecast'
    os.makedirs(output_dir, exist_ok=True)
    save_path = os.path.join(output_dir, 'forecast.png')
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f'\n图表已保存至: {save_path}')
    plt.show()


if __name__ == "__main__":
    plot_temperature_trend()