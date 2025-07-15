import pandas as pd
from typing import Dict
import re

class DataAnalyzer:
    
    def __init__(self, data: pd.DataFrame):
        self.data = data.copy()
        self.clean_data()
    
    def clean_data(self) -> None:
        if self.data.empty:
            return
            
        # 处理财富值：直接使用数值字段
        if 'wealth' in self.data.columns:
            self.data['wealth_numeric'] = pd.to_numeric(self.data['wealth'], errors='coerce').fillna(0)
        
        # 处理年龄：提取数字部分
        if 'age' in self.data.columns:
            self.data['age_numeric'] = self.data['age'].apply(self._extract_age_value)
        
        # 清理行业数据
        if 'industry' in self.data.columns:
            self.data['industry_clean'] = self.data['industry'].apply(self._clean_industry)
            
        # 清理地区数据 - 使用总部或常住地
        if 'headquarters' in self.data.columns:
            self.data['location_clean'] = self.data['headquarters'].apply(self._clean_location)
        elif 'permanent_place' in self.data.columns:
            self.data['location_clean'] = self.data['permanent_place'].apply(self._clean_location)
        elif 'birth_place' in self.data.columns:
            self.data['location_clean'] = self.data['birth_place'].apply(self._clean_location)
    
    def _extract_wealth_value(self, wealth_str: str) -> float:
        if pd.isna(wealth_str):
            return 0
        

        numbers = re.findall(r'\d+\.?\d*', str(wealth_str))
        if numbers:
            return float(numbers[0])
        return 0
    
    def _extract_age_value(self, age_str: str) -> int:
        if pd.isna(age_str):
            return 0
        
        numbers = re.findall(r'\d+', str(age_str))
        if numbers:
            return int(numbers[0])
        return 0
    
    def _clean_industry(self, industry_str: str) -> str:
        if pd.isna(industry_str):
            return "未知"
        return str(industry_str).strip()
    
    def _clean_location(self, location_str: str) -> str:
        if pd.isna(location_str):
            return "未知"
        return str(location_str).strip()
    
    def analyze_industry(self) -> Dict:
        if 'industry_clean' not in self.data.columns:
            return {}
        

        industry_count = self.data['industry_clean'].value_counts()
        

        industry_wealth = {}
        if 'wealth_numeric' in self.data.columns:
            industry_wealth = self.data.groupby('industry_clean')['wealth_numeric'].agg([
                'sum', 'mean', 'count'
            ]).round(2)
        
        return {
            'industry_count': industry_count.to_dict(),
            'industry_wealth': industry_wealth.to_dict() if hasattr(industry_wealth, 'to_dict') else {}
        }
    
    def analyze_age_distribution(self) -> Dict:
        if 'age_numeric' not in self.data.columns:
            return {}
        
        valid_ages = self.data[self.data['age_numeric'] > 0]['age_numeric']
        
        if valid_ages.empty:
            return {}
        
        # 年龄段分组
        age_bins = [0, 30, 40, 50, 60, 70, 100]
        age_labels = ['30岁以下', '30-40岁', '40-50岁', '50-60岁', '60-70岁', '70岁以上']
        
        age_groups = pd.cut(valid_ages, bins=age_bins, labels=age_labels, right=False)
        age_distribution = age_groups.value_counts()
        
        return {
            'age_distribution': age_distribution.to_dict(),
            'age_stats': {
                'mean': valid_ages.mean(),
                'median': valid_ages.median(),
                'std': valid_ages.std(),
                'min': valid_ages.min(),
                'max': valid_ages.max()
            }
        }
    
    def analyze_gender_distribution(self) -> Dict:
        if 'gender' not in self.data.columns:
            return {}
        
        gender_count = self.data['gender'].value_counts()
        
        # 计算性别与财富的关系
        gender_wealth = {}
        if 'wealth_numeric' in self.data.columns:
            gender_wealth = self.data.groupby('gender')['wealth_numeric'].agg([
                'sum', 'mean', 'count'
            ]).round(2)
        
        return {
            'gender_count': gender_count.to_dict(),
            'gender_wealth': gender_wealth.to_dict() if hasattr(gender_wealth, 'to_dict') else {}
        }
    
    def analyze_location_distribution(self) -> Dict:
        if 'location_clean' not in self.data.columns:
            return {}
        
        # 统计各地区富豪数量
        location_count = self.data['location_clean'].value_counts()
        
        # 统计各地区财富总值
        location_wealth = {}
        if 'wealth_numeric' in self.data.columns:
            location_wealth = self.data.groupby('location_clean')['wealth_numeric'].agg([
                'sum', 'mean', 'count'
            ]).round(2)
        
        return {
            'location_count': location_count.to_dict(),
            'location_wealth': location_wealth.to_dict() if hasattr(location_wealth, 'to_dict') else {}
        }
    
    def analyze_wealth_distribution(self) -> Dict:
        if 'wealth_numeric' not in self.data.columns:
            return {}
        
        valid_wealth = self.data[self.data['wealth_numeric'] > 0]['wealth_numeric']
        
        if valid_wealth.empty:
            return {}
        
        # 财富段分组
        wealth_bins = [0, 20, 50, 100, 200, 500, float('inf')]
        wealth_labels = ['20亿以下', '20-50亿', '50-100亿', '100-200亿', '200-500亿', '500亿以上']
        
        wealth_groups = pd.cut(valid_wealth, bins=wealth_bins, labels=wealth_labels, right=False)
        wealth_distribution = wealth_groups.value_counts()
        
        return {
            'wealth_distribution': wealth_distribution.to_dict(),
            'wealth_stats': {
                'mean': valid_wealth.mean(),
                'median': valid_wealth.median(),
                'std': valid_wealth.std(),
                'min': valid_wealth.min(),
                'max': valid_wealth.max(),
                'total': valid_wealth.sum()
            }
        }
    
    def get_top_lists(self, top_n: int = 10) -> Dict:
        result = {}
        
        # 财富榜前N
        if 'wealth_numeric' in self.data.columns:
            top_wealth = self.data.nlargest(top_n, 'wealth_numeric')[
                ['name', 'wealth_numeric', 'industry_clean', 'location_clean'] if all(col in self.data.columns for col in ['name', 'wealth_numeric', 'industry_clean', 'location_clean'])
                else [col for col in ['name', 'wealth_numeric'] if col in self.data.columns]
            ]
            result['top_wealth'] = top_wealth.to_dict('records')
        
        # 最年轻富豪前N
        if 'age_numeric' in self.data.columns:
            youngest = self.data[self.data['age_numeric'] > 0].nsmallest(top_n, 'age_numeric')[
                ['name', 'age_numeric', 'wealth_numeric', 'industry_clean'] if all(col in self.data.columns for col in ['name', 'age_numeric', 'wealth_numeric', 'industry_clean'])
                else [col for col in ['name', 'age_numeric'] if col in self.data.columns]
            ]
            result['youngest'] = youngest.to_dict('records')
        
        return result
    
    def save_cleaned_data(self, filename: str = "hurun_cleaned_data.csv") -> None:
        if self.data.empty:
            print("没有数据可保存")
            return
            
        self.data.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"清洗后数据已保存到 {filename}")
    
    def comprehensive_analysis(self) -> Dict:
        return {
            'basic_stats': {
                'total_count': len(self.data),
                'columns': list(self.data.columns)
            },
            'industry_analysis': self.analyze_industry(),
            'age_analysis': self.analyze_age_distribution(),
            'gender_analysis': self.analyze_gender_distribution(),
            'location_analysis': self.analyze_location_distribution(),
            'wealth_analysis': self.analyze_wealth_distribution(),
            'top_lists': self.get_top_lists()
        } 