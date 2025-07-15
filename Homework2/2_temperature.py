import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 设置中文字体支持
plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题

# 设置全局字体大小
plt.rcParams.update({
    "font.size": 12,  # 全局字体大小
    "axes.titlesize": 16,  # 标题字体大小
    "axes.labelsize": 14,  # 坐标轴标签字体大小
    "xtick.labelsize": 12,  # x轴刻度标签字体大小
    "ytick.labelsize": 12,  # y轴刻度标签字体大小
    "legend.fontsize": 12,  # 图例字体大小
})


def plot_temperature_trend(
        data_path=r"E:\Users\lzr20\PycharmProjects\pythonProject2\weather_data\dalian_weather_data.csv"):
    """
    读取天气数据并绘制2022-2024年平均气温变化趋势图，同时输出每月平均最高和最低温度到文件

    参数:
        data_path: 天气数据CSV文件路径
    """
    # 检查数据文件是否存在
    if not os.path.exists(data_path):
        print(f"错误: 找不到数据文件 '{data_path}'")
        print("请先运行爬虫程序获取天气数据")
        return

    # 读取数据
    try:
        df = pd.read_csv(data_path)
        print(f"成功读取数据，共 {len(df)} 条记录")
    except Exception as e:
        print(f"读取数据时出错: {e}")
        return

    # 数据预处理
    print("正在处理数据...")

    # 转换日期格式
    try:
        df['date'] = pd.to_datetime(df['date'], format='%Y年%m月%d日')
        print("日期格式转换成功")
    except Exception as e:
        print(f"日期格式转换失败: {e}")
        print("请检查数据中的日期格式是否为 'YYYY年MM月DD日'")
        return

    # 提取年份和月份
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month

    # 筛选2022-2024年的数据
    target_years = [2022, 2023, 2024]
    filtered_df = df[df['year'].isin(target_years)]

    if filtered_df.empty:
        print("错误: 数据中不包含2022-2024年的记录")
        return

    # 计算每月平均最高和最低气温
    monthly_avg = filtered_df.groupby(['year', 'month']).agg({
        'max_temperature': 'mean',
        'min_temperature': 'mean'
    }).reset_index()

    # 将年份和月份转换为整数类型（去除小数点）
    monthly_avg['year'] = monthly_avg['year'].astype(int)
    monthly_avg['month'] = monthly_avg['month'].astype(int)

    # 重命名列
    monthly_avg.columns = ['年份', '月份', '平均最高气温', '平均最低气温']

    # 将每月平均最高和最低温度保存到weather_data目录下
    output_csv_path = os.path.join(os.path.dirname(data_path), "monthly_avg_temperature.csv")
    monthly_avg.to_csv(output_csv_path, index=False, encoding='utf-8')
    print(f"每月平均最高和最低温度已保存到: {output_csv_path}")

    # 创建图表
    plt.figure(figsize=(14, 10))  # 增大画布尺寸

    # 绘制平均最高气温趋势
    ax1 = plt.subplot(2, 1, 1)
    for year in target_years:
        year_data = monthly_avg[monthly_avg['年份'] == year]
        # 使用不同颜色和线条样式区分年份
        if year == 2022:
            plt.plot(year_data['月份'], year_data['平均最高气温'], 'o-', color='#1f77b4', linewidth=2.5,
                     label=f"{year}年")
        elif year == 2023:
            plt.plot(year_data['月份'], year_data['平均最高气温'], 's-', color='#ff7f0e', linewidth=2.5,
                     label=f"{year}年")
        else:
            plt.plot(year_data['月份'], year_data['平均最低气温'], '^-', color='#2ca02c', linewidth=2.5,
                     label=f"{year}年")

    # 设置子图标题和标签
    ax1.set_title('2022-2024年大连市每月平均最高气温变化趋势', fontsize=18, pad=15)
    ax1.set_ylabel('温度 (°C)', fontsize=15)
    ax1.legend(fontsize=13, frameon=False)  # 移除图例边框
    ax1.grid(True, linestyle='--', alpha=0.6, linewidth=1)  # 调整网格线样式

    # 设置x轴刻度为月份
    ax1.set_xticks(range(1, 13))
    ax1.set_xticklabels(range(1, 13), fontsize=13)

    # 绘制平均最低气温趋势
    ax2 = plt.subplot(2, 1, 2)
    for year in target_years:
        year_data = monthly_avg[monthly_avg['年份'] == year]
        if year == 2022:
            plt.plot(year_data['月份'], year_data['平均最低气温'], 'o-', color='#1f77b4', linewidth=2.5,
                     label=f"{year}年")
        elif year == 2023:
            plt.plot(year_data['月份'], year_data['平均最低气温'], 's-', color='#ff7f0e', linewidth=2.5,
                     label=f"{year}年")
        else:
            plt.plot(year_data['月份'], year_data['平均最低气温'], '^-', color='#2ca02c', linewidth=2.5,
                     label=f"{year}年")

    # 设置子图标题和标签
    ax2.set_title('2022-2024年大连市每月平均最低气温变化趋势', fontsize=18, pad=15)
    ax2.set_xlabel('月份', fontsize=15)
    ax2.set_ylabel('温度 (°C)', fontsize=15)
    ax2.legend(fontsize=13, frameon=False)
    ax2.grid(True, linestyle='--', alpha=0.6, linewidth=1)

    # 设置x轴刻度为月份
    ax2.set_xticks(range(1, 13))
    ax2.set_xticklabels(range(1, 13), fontsize=13)

    # 调整子图间距
    plt.subplots_adjust(hspace=0.3)

    # 保存图表
    output_dir = "weather_plots/temperature"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    plot_path = os.path.join(output_dir, "temperature_2022-2024.png")
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')

    print(f"图表已保存到: {plot_path}")

    # 显示图表
    plt.show()


if __name__ == "__main__":
    plot_temperature_trend()