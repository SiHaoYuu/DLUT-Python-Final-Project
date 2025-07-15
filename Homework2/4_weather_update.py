import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 设置中文字体
plt.rcParams["font.family"] = ["SimHei", "Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["figure.dpi"] = 300


def plot_weather_heatmap(data_path="weather_data/dalian_weather_data.csv"):
    """
    绘制天气组合热力图（基于"天气1 / 天气2"格式拆分）
    """
    # 检查文件是否存在
    if not os.path.exists(data_path):
        print(f"错误：未找到数据文件 {data_path}")
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
    except Exception as e:
        print(f"日期转换失败：{e}")
        return

    # 提取年份和月份
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month

    # 筛选2022-2024年数据
    target_years = [2022, 2023, 2024]
    filtered_df = df[df["year"].isin(target_years)]
    if filtered_df.empty:
        print("错误：无2022-2024年数据")
        return

    # 天气状况列名
    weather_col = "weather"
    if weather_col not in filtered_df.columns:
        print(f"错误：未找到'{weather_col}'列")
        return

    # 创建保存目录
    output_dir = "weather_plots/weather"
    os.makedirs(output_dir, exist_ok=True)

    # 1. 月度热力图
    for year in target_years:
        for month in range(1, 13):
            # 筛选当月数据
            month_data = filtered_df[(filtered_df["year"] == year) & (filtered_df["month"] == month)]
            if month_data.empty:
                print(f"警告：{year}年{month}月无数据，跳过")
                continue

            # 初始化天气组合计数器
            weather_combinations = {}

            # 统计每种天气组合出现的次数
            for _, row in month_data.iterrows():
                weather_str = row[weather_col]
                if pd.isna(weather_str):
                    continue

                # 按斜杠拆分天气（如"多云 / 晴"拆分为["多云", "晴"]）
                weathers = [w.strip() for w in weather_str.split('/') if w.strip()]

                if len(weathers) >= 2:
                    # 天气1作为横坐标，天气2作为纵坐标
                    weather1 = weathers[0]
                    weather2 = weathers[1]

                    # 更新组合计数
                    if (weather1, weather2) not in weather_combinations:
                        weather_combinations[(weather1, weather2)] = 0
                    weather_combinations[(weather1, weather2)] += 1

            # 如果没有有效的天气组合，跳过绘图
            if not weather_combinations:
                print(f"警告：{year}年{month}月无有效天气组合数据，跳过")
                continue

            # 获取所有唯一的天气状况
            all_weathers = sorted(list(set(
                [w for pair in weather_combinations.keys() for w in pair]
            )))

            # 构建热力图矩阵
            matrix_df = pd.DataFrame(0, index=all_weathers, columns=all_weathers)
            for (weather1, weather2), count in weather_combinations.items():
                matrix_df.loc[weather2, weather1] = count  # 天气2作为纵坐标，天气1作为横坐标

            # 绘制热力图
            plt.figure(figsize=(max(10, len(all_weathers) * 0.8), max(8, len(all_weathers) * 0.6)))
            ax = sns.heatmap(
                matrix_df,
                annot=True,
                fmt="d",
                cmap="YlGnBu",
                cbar_kws={"label": "出现天数"},
                linewidths=0.5,
                square=True
            )

            # 设置标题和标签
            ax.set_title(f"{year}年{month}月大连市天气组合热力图", fontsize=16, pad=20)
            ax.set_xlabel("白天天气情况", fontsize=14, labelpad=15)
            ax.set_ylabel("晚上天气情况", fontsize=14, labelpad=15)

            # 旋转x轴标签避免重叠
            plt.xticks(rotation=45, ha="right")

            plt.tight_layout()

            # 保存图片
            save_path = os.path.join(output_dir, f"weather_update_{year}_{month:02d}.png")
            plt.savefig(save_path)
            plt.close()
            print(f"已生成 {year}年{month}月天气组合热力图：{save_path}")

    # 2. 年度汇总热力图
    for year in target_years:
        # 筛选当年数据
        year_data = filtered_df[filtered_df["year"] == year]
        if year_data.empty:
            print(f"警告：{year}年无数据，跳过")
            continue

        # 初始化年度天气组合计数器
        yearly_combinations = {}

        # 统计全年天气组合
        for _, row in year_data.iterrows():
            weather_str = row[weather_col]
            if pd.isna(weather_str):
                continue

            weathers = [w.strip() for w in weather_str.split('/') if w.strip()]

            if len(weathers) >= 2:
                weather1 = weathers[0]
                weather2 = weathers[1]

                if (weather1, weather2) not in yearly_combinations:
                    yearly_combinations[(weather1, weather2)] = 0
                yearly_combinations[(weather1, weather2)] += 1

        if not yearly_combinations:
            print(f"警告：{year}年无有效天气组合数据，跳过")
            continue

        # 获取所有唯一的天气状况
        all_weathers_yearly = sorted(list(set(
            [w for pair in yearly_combinations.keys() for w in pair]
        )))

        # 构建年度热力图矩阵
        yearly_matrix_df = pd.DataFrame(0, index=all_weathers_yearly, columns=all_weathers_yearly)
        for (weather1, weather2), count in yearly_combinations.items():
            yearly_matrix_df.loc[weather2, weather1] = count

        # 绘制年度热力图
        plt.figure(figsize=(max(12, len(all_weathers_yearly) * 0.8), max(10, len(all_weathers_yearly) * 0.6)))
        ax = sns.heatmap(
            yearly_matrix_df,
            annot=True,
            fmt="d",
            cmap="YlOrRd",
            cbar_kws={"label": "全年出现天数"},
            linewidths=0.5,
            square=True
        )

        ax.set_title(f"{year}年大连市天气组合汇总热力图", fontsize=16, pad=20)
        ax.set_xlabel("白天天气情况", fontsize=14, labelpad=15)
        ax.set_ylabel("晚上天气状况", fontsize=14, labelpad=15)
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        # 保存年度图
        save_path = os.path.join(output_dir, f"weather_update_{year}_summary.png")
        plt.savefig(save_path)
        plt.close()
        print(f"已生成 {year}年天气组合汇总热力图：{save_path}")

    print(f"\n所有天气组合热力图已保存至 {output_dir}")


if __name__ == "__main__":
    plot_weather_heatmap()