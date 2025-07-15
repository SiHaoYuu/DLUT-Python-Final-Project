import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# 设置中文字体支持，确保图表中文显示正常
plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示异常问题

# 设置图片清晰度，让图表细节更清晰
plt.rcParams["figure.dpi"] = 300

def plot_wind_distribution(data_path=r"E:\Users\lzr20\PycharmProjects\pythonProject2\weather_data\dalian_weather_data.csv"):
    """
    绘制2022-2024年每月及每年风力等级分布饼图，优化布局和图例显示
    :param data_path: 天气数据CSV文件路径
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

    # 转换日期格式，按“年-月-日”格式解析
    try:
        df['date'] = pd.to_datetime(df['date'], format='%Y年%m月%d日')
        print("日期格式转换成功")
    except Exception as e:
        print(f"日期格式转换失败: {e}")
        print("请检查数据中的日期格式是否为 'YYYY年MM月DD日'")
        return

    # 提取年份和月份信息，方便后续分组统计
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month

    # 筛选2022-2024年的数据，限定分析时间范围
    target_years = [2022, 2023, 2024]
    filtered_df = df[df['year'].isin(target_years)]

    if filtered_df.empty:
        print("错误: 数据中不包含2022-2024年的记录")
        return

    # 从wind_day和wind_night中提取风力等级，处理带“级”的文本
    def extract_wind_level(wind_str):
        if pd.isna(wind_str):
            return np.nan
        try:
            if '级' in wind_str:
                # 处理“X-X级”格式，取较大值；处理“X级”格式，直接取数值
                if '-' in wind_str:
                    return int(wind_str.split('-')[1].replace('级', ''))
                else:
                    return int(wind_str.replace('级', ''))
            else:
                return np.nan
        except:
            return np.nan

    # 提取白天和夜间的风力等级
    filtered_df['wind_level_day'] = filtered_df['wind_day'].apply(extract_wind_level)
    filtered_df['wind_level_night'] = filtered_df['wind_night'].apply(extract_wind_level)

    # 计算每天的最高风力等级，取白天和夜间的最大值
    filtered_df['max_wind_level'] = filtered_df[['wind_level_day', 'wind_level_night']].max(axis=1)

    # 定义风力等级区间，划分不同风力等级
    wind_bins = [0, 3, 5, 7, 10, np.inf]
    wind_labels = ['0-3级', '4-5级', '6-7级', '8-10级', '10级以上']

    # 将风力等级划分为区间，便于统计分布
    filtered_df['wind_category'] = pd.cut(
        filtered_df['max_wind_level'],
        bins=wind_bins,
        labels=wind_labels,
        right=False
    )

    # 计算每个月不同风力等级的天数，按年、月、风力等级分组统计
    monthly_wind_counts = filtered_df.groupby(['year', 'month', 'wind_category']).size().unstack(fill_value=0)

    # 创建图表保存目录，存放生成的饼图
    output_dir = "weather_plots/wind"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 为每个月创建饼图
    for year in target_years:
        for month in range(1, 13):
            if (year, month) in monthly_wind_counts.index:
                wind_data = monthly_wind_counts.loc[(year, month)]
                if wind_data.sum() == 0:
                    continue  # 跳过无数据的月份

                # 智能标签：占比小于3%时不显示百分比，避免重叠
                def autopct_format(pct):
                    return f'{pct:.1f}%' if pct >= 3 else ''

                plt.figure(figsize=(8, 8))  # 设定饼图画布大小，保证圆形展示
                wedges, texts, autotexts = plt.pie(
                    wind_data,
                    autopct=autopct_format,
                    startangle=90,  # 饼图起始角度，让0-3级在正上方
                    colors=['#98FB98', '#87CEEB', '#FFD700', '#FFA07A', '#FF6347'],  # 不同风力等级配色
                    wedgeprops={'edgecolor': 'w', 'linewidth': 1},  # 扇区间隔白线，更清晰
                    textprops={'fontsize': 10}  # 标签字体大小
                )

                # 添加图例，放在饼图右侧，清晰展示等级含义
                plt.legend(
                    wedges,
                    wind_data.index,
                    title="风力等级",
                    loc="center left",
                    bbox_to_anchor=(1, 0.5),  # 图例位置，避免遮挡饼图
                    fontsize=10,
                    title_fontsize=12
                )

                plt.title(f'{year}年{month}月大连市风力等级分布', fontsize=14, pad=20)  # 标题与饼图间距加大
                plt.axis('equal')  # 保证饼图是正圆形
                plt.tight_layout()  # 自动优化布局，避免标题、图例重叠

                # 保存图表，按年月命名
                plot_path = os.path.join(output_dir, f'wind_{year}_{month:02d}.png')
                plt.savefig(plot_path, dpi=300, bbox_inches='tight')
                plt.close()
                print(f'已生成 {year}年{month}月 风力分布图: {plot_path}')

    # 为每年创建汇总饼图
    for year in target_years:
        yearly_wind_data = monthly_wind_counts.loc[year].sum()  # 按年汇总风力数据

        # 智能标签，占比小于3%不显示百分比
        def autopct_format(pct):
            return f'{pct:.1f}%' if pct >= 3 else ''

        plt.figure(figsize=(8, 8))
        wedges, texts, autotexts = plt.pie(
            yearly_wind_data,
            autopct=autopct_format,
            startangle=90,
            colors=['#98FB98', '#87CEEB', '#FFD700', '#FFA07A', '#FF6347'],
            wedgeprops={'edgecolor': 'w', 'linewidth': 1},
            textprops={'fontsize': 12}
        )

        # 添加图例，放在右侧
        plt.legend(
            wedges,
            yearly_wind_data.index,
            title="风力等级",
            loc="center left",
            bbox_to_anchor=(1, 0.5),
            fontsize=11,
            title_fontsize=13
        )

        plt.title(f'{year}年大连市风力等级分布', fontsize=16, pad=20)
        plt.axis('equal')
        plt.tight_layout()

        # 保存汇总图表
        plot_path = os.path.join(output_dir, f'wind_{year}_summary.png')
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f'已生成 {year}年 风力分布汇总图: {plot_path}')

    print(f"\n所有风力分布图已保存到目录: {output_dir}")

if __name__ == "__main__":
    plot_wind_distribution()