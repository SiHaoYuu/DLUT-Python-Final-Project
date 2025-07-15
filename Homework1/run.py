import sys
import os
import traceback

# 添加src目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.data_collector import DataCollector
from src.data_analyzer import DataAnalyzer
from src.data_visualizer import DataVisualizer
from src.report_generator import ReportGenerator


def main():
    try:
        # 数据采集
        collector = DataCollector()
        raw_data = collector.collect_all_data(max_pages=50)
        
        if not raw_data:
            print("数据采集失败，程序终止")
            return
        
        # 保存原始数据
        collector.save_to_csv("hurun_raw_data.csv")
        
        # 数据分析
        df = collector.get_data_frame()
        analyzer = DataAnalyzer(df)
        
        # 保存清洗后的数据
        analyzer.save_cleaned_data("hurun_cleaned_data.csv")
        
        analysis_results = analyzer.comprehensive_analysis()
        
        print(f"分析完成，共处理 {analysis_results['basic_stats']['total_count']} 条数据")
        
        # 数据可视化
        visualizer = DataVisualizer(output_dir="charts")
        chart_paths = visualizer.create_comprehensive_dashboard(analysis_results)
        
        # 生成报告
        report_generator = ReportGenerator(analysis_results, chart_paths)
        report_file = report_generator.generate_full_report("胡润百富榜分析报告.txt")
        
        # 输出结果摘要
        print(f"原始数据文件：hurun_raw_data.csv")
        print(f"清洗后数据文件：hurun_cleaned_data.csv")
        print(f"图表目录：charts/")
        print(f"分析报告：{report_file}")
        print(f"图表数量：{len(chart_paths)}")
        
        import os
        for chart_path in chart_paths:
            if os.path.exists(chart_path):
                print(f"图表文件：{chart_path}")
        
        if os.path.exists("hurun_raw_data.csv"):
            print("原始数据文件：hurun_raw_data.csv")
        if os.path.exists("hurun_cleaned_data.csv"):
            print("清洗后数据文件：hurun_cleaned_data.csv")
        if os.path.exists(report_file):
            print(f"分析报告：{report_file}")
        
        # 行业分析
        industry_analysis = analysis_results.get('industry_analysis', {})
        if industry_analysis.get('industry_count'):
            top_industry = list(industry_analysis['industry_count'].items())[0]
            print(f"主要行业：{top_industry[0]}（{top_industry[1]}人）")
        
        # 财富统计
        wealth_analysis = analysis_results.get('wealth_analysis', {})
        if wealth_analysis.get('wealth_stats'):
            wealth_stats = wealth_analysis['wealth_stats']
            print(f"平均财富：{wealth_stats.get('mean', 0):.2f}亿元")
            print(f"财富总值：{wealth_stats.get('total', 0):.2f}亿元")
        
        # 年龄统计
        age_analysis = analysis_results.get('age_analysis', {})
        if age_analysis.get('age_stats'):
            age_stats = age_analysis['age_stats']
            print(f"平均年龄：{age_stats.get('mean', 0):.1f}岁")
        
        # 地区分布
        location_analysis = analysis_results.get('location_analysis', {})
        if location_analysis.get('location_count'):
            top_location = list(location_analysis['location_count'].items())[0]
            print(f"主要地区：{top_location[0]}（{top_location[1]}人）")
        
        print("\n数据分析项目执行成功！")
        
    except KeyboardInterrupt:
        print("\n用户中断执行")
    except Exception as e:
        print(f"\n程序执行出错：{e}")
        print("详细错误信息：")
        traceback.print_exc()
    finally:
        print("\完成")


if __name__ == "__main__":
    main() 