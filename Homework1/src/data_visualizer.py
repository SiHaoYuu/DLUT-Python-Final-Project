import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from typing import Dict, List, Optional
import os
from .font_helper import setup_chinese_font

# 设置seaborn样式
sns.set_style("whitegrid")
sns.set_palette("husl")


class DataVisualizer:
    
    def __init__(self, output_dir: str = "charts"):
        self.output_dir = output_dir
        self.ensure_output_dir()
        
    def ensure_output_dir(self) -> None:
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def plot_industry_distribution(self, industry_data: Dict, save_path: Optional[str] = None) -> str:
        if not industry_data.get('industry_count'):
            return ""
        
        # 确保中文字体设置
        setup_chinese_font()
        
        # 获取前15个行业
        industry_count = dict(list(industry_data['industry_count'].items())[:15])
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # 柱状图
        industries = list(industry_count.keys())
        counts = list(industry_count.values())
        
        bars = ax1.bar(range(len(industries)), counts, color='skyblue', alpha=0.8)
        ax1.set_xlabel('行业')
        ax1.set_ylabel('富豪数量')
        ax1.set_title('各行业富豪数量分布（前15名）')
        ax1.set_xticks(range(len(industries)))
        ax1.set_xticklabels(industries, rotation=45, ha='right')
        
        # 在柱子上添加数值标签
        for bar, count in zip(bars, counts):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{count}', ha='center', va='bottom')
        
        # 饼图（前10个行业）
        top_10_industry = dict(list(industry_count.items())[:10])
        others_items = list(industry_count.items())[10:]
        others_count = sum([count for _, count in others_items]) if others_items else 0
        if others_count > 0:
            top_10_industry['其他'] = others_count
        
        wedges, texts, autotexts = ax2.pie(
            top_10_industry.values(), 
            labels=top_10_industry.keys(),
            autopct='%1.1f%%',
            startangle=90
        )
        ax2.set_title('各行业富豪占比分布（前10名）')
        
        plt.tight_layout()
        
        if not save_path:
            save_path = os.path.join(self.output_dir, 'industry_distribution.png')
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return save_path
    
    def plot_wealth_distribution(self, wealth_data: Dict, save_path: Optional[str] = None) -> str:
        if not wealth_data.get('wealth_distribution'):
            return ""
        
        # 确保中文字体设置
        setup_chinese_font()
        
        wealth_dist = wealth_data['wealth_distribution']
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # 财富段分布柱状图
        segments = list(wealth_dist.keys())
        counts = list(wealth_dist.values())
        
        bars = ax1.bar(range(len(segments)), counts, color='lightcoral', alpha=0.8)
        ax1.set_xlabel('财富区间')
        ax1.set_ylabel('富豪数量')
        ax1.set_title('财富分布情况')
        ax1.set_xticks(range(len(segments)))
        ax1.set_xticklabels(segments, rotation=45, ha='right')
        
        # 添加数值标签
        for bar, count in zip(bars, counts):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{count}', ha='center', va='bottom')
        
        # 财富统计信息
        if wealth_data.get('wealth_stats'):
            stats = wealth_data['wealth_stats']
            stats_text = f"""财富统计信息：
平均值：{stats.get('mean', 0):.2f}亿
中位数：{stats.get('median', 0):.2f}亿
标准差：{stats.get('std', 0):.2f}亿
最小值：{stats.get('min', 0):.2f}亿
最大值：{stats.get('max', 0):.2f}亿
总财富：{stats.get('total', 0):.2f}亿"""
            
            ax2.text(0.1, 0.9, stats_text, transform=ax2.transAxes, 
                    fontsize=12, verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
            ax2.set_xlim(0, 1)
            ax2.set_ylim(0, 1)
            ax2.axis('off')
            ax2.set_title('财富统计信息')
        
        plt.tight_layout()
        
        if not save_path:
            save_path = os.path.join(self.output_dir, 'wealth_distribution.png')
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return save_path
    
    def plot_age_distribution(self, age_data: Dict, save_path: Optional[str] = None) -> str:
        if not age_data.get('age_distribution'):
            return ""
        
        # 确保中文字体设置
        setup_chinese_font()
        
        age_dist = age_data['age_distribution']
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # 年龄段分布柱状图
        age_groups = list(age_dist.keys())
        counts = list(age_dist.values())
        
        bars = ax1.bar(range(len(age_groups)), counts, color='lightgreen', alpha=0.8)
        ax1.set_xlabel('年龄段')
        ax1.set_ylabel('富豪数量')
        ax1.set_title('年龄分布情况')
        ax1.set_xticks(range(len(age_groups)))
        ax1.set_xticklabels(age_groups, rotation=45, ha='right')
        
        # 添加数值标签
        for bar, count in zip(bars, counts):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{count}', ha='center', va='bottom')
        
        # 年龄统计信息
        if age_data.get('age_stats'):
            stats = age_data['age_stats']
            stats_text = f"""年龄统计信息：
平均年龄：{stats.get('mean', 0):.1f}岁
年龄中位数：{stats.get('median', 0):.1f}岁
年龄标准差：{stats.get('std', 0):.1f}岁
最小年龄：{stats.get('min', 0):.0f}岁
最大年龄：{stats.get('max', 0):.0f}岁"""
            
            ax2.text(0.1, 0.9, stats_text, transform=ax2.transAxes, 
                    fontsize=12, verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
            ax2.set_xlim(0, 1)
            ax2.set_ylim(0, 1)
            ax2.axis('off')
            ax2.set_title('年龄统计信息')
        
        plt.tight_layout()
        
        if not save_path:
            save_path = os.path.join(self.output_dir, 'age_distribution.png')
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return save_path
    
    def plot_location_heatmap(self, location_data: Dict, save_path: Optional[str] = None) -> str:
        if not location_data.get('location_count'):
            return ""
        
        # 确保中文字体设置
        setup_chinese_font()
        
        location_count = location_data['location_count']
        
        # 获取前20个地区
        top_locations = dict(list(location_count.items())[:20])
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # 创建热力图数据
        locations = list(top_locations.keys())
        counts = list(top_locations.values())
        
        # 创建矩阵用于热力图显示
        matrix_size = int(np.ceil(np.sqrt(len(locations))))
        heat_matrix = np.zeros((matrix_size, matrix_size))
        location_labels = np.empty((matrix_size, matrix_size), dtype=object)
        
        for i, (loc, count) in enumerate(top_locations.items()):
            row = i // matrix_size
            col = i % matrix_size
            heat_matrix[row, col] = count
            location_labels[row, col] = f"{loc}\n({count})"
        
        # 绘制热力图
        sns.heatmap(heat_matrix, annot=location_labels, fmt='', 
                   cmap='YlOrRd', ax=ax, cbar_kws={'label': '富豪数量'})
        ax.set_title('各地区富豪分布热力图（前20名）')
        ax.set_xlabel('')
        ax.set_ylabel('')
        
        plt.tight_layout()
        
        if not save_path:
            save_path = os.path.join(self.output_dir, 'location_heatmap.png')
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return save_path
    
    def plot_gender_distribution(self, gender_data: Dict, save_path: Optional[str] = None) -> str:
        if not gender_data.get('gender_count'):
            return ""
        
        # 确保中文字体设置
        setup_chinese_font()
        
        gender_count = gender_data['gender_count']
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # 性别分布饼图
        genders = list(gender_count.keys())
        counts = list(gender_count.values())
        
        wedges, texts, autotexts = ax1.pie(
            counts, labels=genders, autopct='%1.1f%%',
            startangle=90, colors=['lightblue', 'lightpink']
        )
        ax1.set_title('性别分布情况')
        
        # 性别与财富关系
        if gender_data.get('gender_wealth'):
            wealth_stats = gender_data['gender_wealth']
            if 'mean' in wealth_stats:
                gender_means = wealth_stats['mean']
                genders_wealth = list(gender_means.keys())
                means = list(gender_means.values())
                
                bars = ax2.bar(genders_wealth, means, color=['lightblue', 'lightpink'], alpha=0.8)
                ax2.set_xlabel('性别')
                ax2.set_ylabel('平均财富值（亿）')
                ax2.set_title('不同性别平均财富对比')
                
                # 添加数值标签
                for bar, mean_val in zip(bars, means):
                    height = bar.get_height()
                    ax2.text(bar.get_x() + bar.get_width()/2., height + 1,
                            f'{mean_val:.1f}', ha='center', va='bottom')
        
        plt.tight_layout()
        
        if not save_path:
            save_path = os.path.join(self.output_dir, 'gender_distribution.png')
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return save_path
    
    def create_comprehensive_dashboard(self, analysis_results: Dict) -> List[str]:
        chart_paths = []
        
        # 行业分布图
        if analysis_results.get('industry_analysis'):
            path = self.plot_industry_distribution(analysis_results['industry_analysis'])
            if path:
                chart_paths.append(path)
        
        # 财富分布图
        if analysis_results.get('wealth_analysis'):
            path = self.plot_wealth_distribution(analysis_results['wealth_analysis'])
            if path:
                chart_paths.append(path)
        
        # 年龄分布图
        if analysis_results.get('age_analysis'):
            path = self.plot_age_distribution(analysis_results['age_analysis'])
            if path:
                chart_paths.append(path)
        
        # 地区热力图
        if analysis_results.get('location_analysis'):
            path = self.plot_location_heatmap(analysis_results['location_analysis'])
            if path:
                chart_paths.append(path)
        
        # 性别分布图
        if analysis_results.get('gender_analysis'):
            path = self.plot_gender_distribution(analysis_results['gender_analysis'])
            if path:
                chart_paths.append(path)
        
        print(f"共生成 {len(chart_paths)} 个图表")
        return chart_paths 