
from typing import Dict, List
import datetime
import os


class ReportGenerator:
    
    def __init__(self, analysis_results: Dict, chart_paths: List[str]):
        self.analysis_results = analysis_results
        self.chart_paths = chart_paths
        self.report_content = []
        
    def generate_executive_summary(self) -> str:
        basic_stats = self.analysis_results.get('basic_stats', {})
        total_count = basic_stats.get('total_count', 0)
        
        summary = f"""## 数据概况

**基本信息：**
- 样本总数：{total_count}人
- 数据来源：胡润百富榜官方网站
- 分析时间：{datetime.datetime.now().strftime('%Y年%m月%d日')}

**关键数据：**
"""
        
        # 行业分析摘要
        industry_analysis = self.analysis_results.get('industry_analysis', {})
        if industry_analysis.get('industry_count'):
            top_industry = list(industry_analysis['industry_count'].items())[0]
            summary += f"- 最主要的行业是{top_industry[0]}，拥有{top_industry[1]}位富豪\n"
        
        # 财富分析摘要
        wealth_analysis = self.analysis_results.get('wealth_analysis', {})
        if wealth_analysis.get('wealth_stats'):
            wealth_stats = wealth_analysis['wealth_stats']
            summary += f"- 平均财富值为{wealth_stats.get('mean', 0):.2f}亿元\n"
            summary += f"- 财富总值达到{wealth_stats.get('total', 0):.2f}亿元\n"
        
        # 年龄分析摘要
        age_analysis = self.analysis_results.get('age_analysis', {})
        if age_analysis.get('age_stats'):
            age_stats = age_analysis['age_stats']
            summary += f"- 富豪平均年龄为{age_stats.get('mean', 0):.1f}岁\n"
        
        # 地区分析摘要
        location_analysis = self.analysis_results.get('location_analysis', {})
        if location_analysis.get('location_count'):
            top_location = list(location_analysis['location_count'].items())[0]
            summary += f"- 富豪最集中的地区是{top_location[0]}，拥有{top_location[1]}位富豪\n"
        
        return summary
    
    def generate_industry_analysis(self) -> str:
        industry_analysis = self.analysis_results.get('industry_analysis', {})
        if not industry_analysis:
            return "## 行业分析\n\n暂无行业数据可供分析。\n"
        
        content = "## 行业分析\n\n"
        
        # 行业分布统计
        industry_count = industry_analysis.get('industry_count', {})
        if industry_count:
            content += "### 各行业富豪数量分布\n\n"
            for i, (industry, count) in enumerate(list(industry_count.items())[:10], 1):
                content += f"{i}. {industry}：{count}人\n"
            content += "\n"
        
        # 行业财富分析
        industry_wealth = industry_analysis.get('industry_wealth', {})
        if industry_wealth and 'sum' in industry_wealth:
            content += "### 各行业财富总值排名\n\n"
            wealth_sum = industry_wealth['sum']
            sorted_wealth = sorted(wealth_sum.items(), key=lambda x: x[1], reverse=True)
            
            for i, (industry, total_wealth) in enumerate(sorted_wealth[:10], 1):
                avg_wealth = industry_wealth.get('mean', {}).get(industry, 0)
                content += f"{i}. {industry}：总财富 {total_wealth:.2f}亿元，平均财富 {avg_wealth:.2f}亿元\n"
            content += "\n"
        
        return content
    
    def generate_demographic_analysis(self) -> str:
        content = "## 人口统计分析\n\n"
        
        # 年龄分析
        age_analysis = self.analysis_results.get('age_analysis', {})
        if age_analysis:
            content += "### 年龄结构分析\n\n"
            
            age_stats = age_analysis.get('age_stats', {})
            if age_stats:
                content += f"**年龄统计指标：**\n"
                content += f"- 平均年龄：{age_stats.get('mean', 0):.1f}岁\n"
                content += f"- 年龄中位数：{age_stats.get('median', 0):.1f}岁\n"
                content += f"- 最年轻：{age_stats.get('min', 0):.0f}岁\n"
                content += f"- 最年长：{age_stats.get('max', 0):.0f}岁\n\n"
            
            age_distribution = age_analysis.get('age_distribution', {})
            if age_distribution:
                content += "**年龄段分布：**\n"
                for age_group, count in age_distribution.items():
                    content += f"- {age_group}：{count}人\n"
                content += "\n"
        
        # 性别分析
        gender_analysis = self.analysis_results.get('gender_analysis', {})
        if gender_analysis:
            content += "### 性别结构分析\n\n"
            
            gender_count = gender_analysis.get('gender_count', {})
            if gender_count:
                total_gender = sum(gender_count.values())
                content += "**性别分布：**\n"
                for gender, count in gender_count.items():
                    percentage = (count / total_gender) * 100 if total_gender > 0 else 0
                    content += f"- {gender}：{count}人（{percentage:.1f}%）\n"
                content += "\n"
            
            gender_wealth = gender_analysis.get('gender_wealth', {})
            if gender_wealth and 'mean' in gender_wealth:
                content += "**性别财富差异：**\n"
                for gender, avg_wealth in gender_wealth['mean'].items():
                    content += f"- {gender}平均财富：{avg_wealth:.2f}亿元\n"
                content += "\n"
        
        # 地区分析
        location_analysis = self.analysis_results.get('location_analysis', {})
        if location_analysis:
            content += "### 地区分布分析\n\n"
            
            location_count = location_analysis.get('location_count', {})
            if location_count:
                content += "**主要地区富豪数量（前10名）：**\n"
                for i, (location, count) in enumerate(list(location_count.items())[:10], 1):
                    content += f"{i}. {location}：{count}人\n"
                content += "\n"
        
        return content
    
    def generate_wealth_analysis(self) -> str:
        wealth_analysis = self.analysis_results.get('wealth_analysis', {})
        if not wealth_analysis:
            return "## 财富分析\n\n暂无财富数据可供分析。\n"
        
        content = "## 财富分析\n\n"
        
        # 财富统计
        wealth_stats = wealth_analysis.get('wealth_stats', {})
        if wealth_stats:
            content += "### 财富统计概况\n\n"
            content += f"**基本统计指标：**\n"
            content += f"- 平均财富：{wealth_stats.get('mean', 0):.2f}亿元\n"
            content += f"- 财富中位数：{wealth_stats.get('median', 0):.2f}亿元\n"
            content += f"- 财富总和：{wealth_stats.get('total', 0):.2f}亿元\n"
            content += f"- 最低财富：{wealth_stats.get('min', 0):.2f}亿元\n"
            content += f"- 最高财富：{wealth_stats.get('max', 0):.2f}亿元\n"
            content += f"- 标准差：{wealth_stats.get('std', 0):.2f}亿元\n\n"
        
        # 财富分布
        wealth_distribution = wealth_analysis.get('wealth_distribution', {})
        if wealth_distribution:
            content += "### 财富区间分布\n\n"
            for wealth_range, count in wealth_distribution.items():
                content += f"- {wealth_range}：{count}人\n"
            content += "\n"
        

        
        return content
    
    def generate_top_lists(self) -> str:
        top_lists = self.analysis_results.get('top_lists', {})
        if not top_lists:
            return "## 排行榜\n\n暂无排行榜数据。\n"
        
        content = "## 排行榜\n\n"
        
        # 财富排行榜
        top_wealth = top_lists.get('top_wealth', [])
        if top_wealth:
            content += "### 财富排行榜（前10名）\n\n"
            for i, person in enumerate(top_wealth[:10], 1):
                name = person.get('name', '未知')
                wealth = person.get('wealth_numeric', 0)
                industry = person.get('industry_clean', '未知')
                location = person.get('location_clean', '未知')
                content += f"{i}. {name} - {wealth:.2f}亿元（{industry}，{location}）\n"
            content += "\n"
        
        # 最年轻富豪排行榜
        youngest = top_lists.get('youngest', [])
        if youngest:
            content += "### 最年轻富豪排行榜（前10名）\n\n"
            for i, person in enumerate(youngest[:10], 1):
                name = person.get('name', '未知')
                age = person.get('age_numeric', 0)
                wealth = person.get('wealth_numeric', 0)
                industry = person.get('industry_clean', '未知')
                content += f"{i}. {name} - {age}岁，{wealth:.2f}亿元（{industry}）\n"
            content += "\n"
        
        return content
    
    def generate_conclusions(self) -> str:
        basic_stats = self.analysis_results.get('basic_stats', {})
        total_count = basic_stats.get('total_count', 0)
        
        content = f"""## 数据汇总

### 分析总数
- 总样本数：{total_count}人

### 行业分布概况
"""
        
        industry_analysis = self.analysis_results.get('industry_analysis', {})
        if industry_analysis.get('industry_count'):
            industry_count = industry_analysis['industry_count']
            content += f"- 涉及行业数量：{len(industry_count)}个\n"
            if industry_count:
                top_industry = list(industry_count.items())[0]
                content += f"- 最大行业：{top_industry[0]}（{top_industry[1]}人）\n"
        
        content += "\n### 财富数据概况\n"
        wealth_analysis = self.analysis_results.get('wealth_analysis', {})
        if wealth_analysis.get('wealth_stats'):
            wealth_stats = wealth_analysis['wealth_stats']
            content += f"- 财富总额：{wealth_stats.get('total', 0):.2f}亿元\n"
            content += f"- 平均财富：{wealth_stats.get('mean', 0):.2f}亿元\n"
            content += f"- 财富中位数：{wealth_stats.get('median', 0):.2f}亿元\n"
        
        content += "\n### 地区分布概况\n"
        location_analysis = self.analysis_results.get('location_analysis', {})
        if location_analysis.get('location_count'):
            location_count = location_analysis['location_count']
            content += f"- 涉及地区数量：{len(location_count)}个\n"
            if location_count:
                top_location = list(location_count.items())[0]
                content += f"- 最大地区：{top_location[0]}（{top_location[1]}人）\n"
        
        content += "\n### 年龄数据概况\n"
        age_analysis = self.analysis_results.get('age_analysis', {})
        if age_analysis.get('age_stats'):
            age_stats = age_analysis['age_stats']
            content += f"- 平均年龄：{age_stats.get('mean', 0):.1f}岁\n"
            content += f"- 年龄范围：{age_stats.get('min', 0):.0f}-{age_stats.get('max', 0):.0f}岁\n"
        
        return content
    
    def generate_full_report(self, output_file: str = "胡润百富榜分析报告.txt") -> str:
        report_sections = [
            f"# 2024年胡润百富榜数据分析报告\n\n",
            f"报告生成时间：{datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}\n\n",
            self.generate_executive_summary(),
            "\n",
            self.generate_industry_analysis(),
            "\n",
            self.generate_demographic_analysis(),
            "\n",
            self.generate_wealth_analysis(),
            "\n",
            self.generate_top_lists(),
            "\n",
            self.generate_conclusions(),
            "\n",
            "## 图表说明\n\n",
            "本报告共生成以下图表文件：\n"
        ]
        
        # 添加图表文件说明
        for i, chart_path in enumerate(self.chart_paths, 1):
            chart_name = os.path.basename(chart_path)
            report_sections.append(f"{i}. {chart_name}\n")
        
        # 合并所有部分
        full_report = "".join(report_sections)
        
        # 保存报告
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(full_report)
        
        print(f"分析报告已生成：{output_file}")
        return output_file 