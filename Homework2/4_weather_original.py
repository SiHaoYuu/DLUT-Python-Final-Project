import pandas as pd
import matplotlib.pyplot as plt
import os

# 设置中文字体，解决中文显示问题
plt.rcParams["font.family"] = ["SimHei", "Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示异常

# 设置图表清晰度
plt.rcParams["figure.dpi"] = 300

def plot_weather_distribution(data_path="weather_data/dalian_weather_data.csv"):
    """
    绘制2022-2024年每月天气状况分布柱状图，优化天气解析和统计逻辑
    :param data_path: 天气数据CSV文件路径
    """
    # 检查文件是否存在
    if not os.path.exists(data_path):
        print(f"错误：未找到数据文件 {data_path}，请先运行爬虫程序")
        return

    # 读取数据
    try:
        df = pd.read_csv(data_path)
        print(f"成功读取 {len(df)} 条数据")
    except Exception as e:
        print(f"读取数据失败：{e}")
        return

    # 转换日期格式
    try:
        df["date"] = pd.to_datetime(df["date"], format="%Y年%m月%d日")
        print("日期格式转换成功")
    except Exception as e:
        print(f"日期转换失败：{e}，请检查日期格式是否为 'YYYY年MM月DD日'")
        return

    # 提取年份和月份
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month

    # 筛选2022-2024年数据
    target_years = [2022, 2023, 2024]
    filtered_df = df[df["year"].isin(target_years)]
    if filtered_df.empty:
        print("错误：数据中无2022-2024年记录")
        return

    # 优化天气状况提取：直接取原始天气描述（若需拆分“转”天气，可根据需求调整）
    # 如需拆分白天/夜间天气，可改为：df["weather"] = df["weather"].str.split("转").str[0]（示例）
    # 这里简化为直接使用原始天气描述统计
    weather_col = "weather"  # 假设CSV中有“weather”列存储天气状况

    # 统计每月天气状况天数（按年、月、天气类型分组）
    monthly_weather = filtered_df.groupby(["year", "month", weather_col]).size().reset_index(name="days")

    # 创建图表保存目录
    output_dir = "weather_plots/weather"
    os.makedirs(output_dir, exist_ok=True)

    # 为每个月绘制柱状图
    for year in target_years:
        for month in range(1, 13):
            # 筛选当前年月数据
            month_data = monthly_weather[(monthly_weather["year"] == year) & (monthly_weather["month"] == month)]
            if month_data.empty:
                continue  # 无数据则跳过

            # 绘制柱状图
            plt.figure(figsize=(10, 6))
            bars = plt.bar(
                month_data[weather_col],  # X轴：天气类型
                month_data["days"],       # Y轴：天数
                color="#4682B4",          # 统一柱状图颜色（可根据天气类型自定义配色）
                edgecolor="black"         # 柱子边框颜色
            )

            # 添加数据标签
            for bar in bars:
                height = bar.get_height()
                plt.text(
                    bar.get_x() + bar.get_width() / 2,
                    height + 0.2,
                    f"{height}天",
                    ha="center",
                    va="bottom",
                    fontsize=9
                )

            # 设置图表属性
            plt.title(f"{year}年{month}月大连市天气状况分布", fontsize=14, pad=20)
            plt.xlabel("天气状况", fontsize=12)
            plt.ylabel("天数", fontsize=12)
            plt.xticks(rotation=45, ha="right", fontsize=10)  # 旋转X轴标签避免重叠
            plt.ylim(0, month_data["days"].max() + 2)         # Y轴留空，避免标签顶到边界

            # 自动调整布局
            plt.tight_layout()

            # 保存图表
            save_path = os.path.join(output_dir, f"weather_original_{year}_{month:02d}.png")
            plt.savefig(save_path)
            plt.close()
            print(f"已生成 {year}年{month}月 天气分布柱状图：{save_path}")

    # 绘制年度汇总柱状图（可选，如需可取消注释）
    for year in target_years:
        yearly_data = monthly_weather[monthly_weather["year"] == year].groupby(weather_col)["days"].sum().reset_index()
        plt.figure(figsize=(12, 7))
        plt.bar(yearly_data[weather_col], yearly_data["days"], color="#FFA07A", edgecolor="black")
        plt.title(f"{year}年大连市天气状况分布汇总", fontsize=16, pad=20)
        plt.xlabel("天气状况", fontsize=13)
        plt.ylabel("总天数", fontsize=13)
        plt.xticks(rotation=45, ha="right", fontsize=11)
        plt.tight_layout()
        save_path = os.path.join(output_dir, f"weather_original_{year}_summary.png")
        plt.savefig(save_path)
        plt.close()
        print(f"已生成 {year}年 天气分布汇总图：{save_path}")

    print(f"\n所有图表已保存至 {output_dir}")

if __name__ == "__main__":
    plot_weather_distribution()