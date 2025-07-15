import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import os
from fake_useragent import UserAgent


class WeatherSpider:
    def __init__(self):
        self.base_url = "https://www.tianqihoubao.com"
        self.ua = UserAgent()
        self.headers = {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive'
        }
        self.city_code = "dalian"  # 大连市的代码，需要根据实际网站结构确认
        self.all_data = []
        self.current_attempts = 0
        self.max_attempts = 3  # 每个页面的最大重试次数

        # 创建数据保存目录
        self.data_dir = os.path.join(os.getcwd(), "weather_data")
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def fetch_weather(self, year, month):
        """获取指定年月的天气数据，增加重试机制和详细日志"""
        url = f"{self.base_url}/lishi/{self.city_code}/month/{year}{month:02d}.html"
        print(f"正在获取 {year}年{month}月 大连天气数据: {url}")

        for attempt in range(self.max_attempts):
            try:
                # 每次请求前随机延迟，避免请求过于频繁
                wait_time = random.uniform(2, 5)
                print(f"等待 {wait_time:.2f} 秒后发送请求...")
                time.sleep(wait_time)

                response = requests.get(url, headers=self.headers, timeout=15)
                response.raise_for_status()
                response.encoding = 'utf-8'

                # 验证响应内容是否包含天气数据
                if "404 Not Found" in response.text or "没有找到" in response.text:
                    print(f"警告: 页面 {url} 返回空内容或404错误")
                    return False

                soup = BeautifulSoup(response.text, 'html.parser')

                # 尝试多种方式定位天气表格
                table = soup.find('table', class_='b')
                if not table:
                    # 备选定位方式
                    table = soup.find('table', class_='table0')

                if not table:
                    # 更通用的定位方式
                    tables = soup.find_all('table')
                    if tables:
                        # 选择行数最多的表格作为天气表格
                        table = max(tables, key=lambda t: len(t.find_all('tr')))
                    else:
                        print(f"错误: 在 {url} 中未找到任何表格")
                        return False

                # 解析表格数据
                rows = table.find_all('tr')[1:]  # 跳过表头
                if not rows:
                    print(f"警告: 在 {url} 中找到表格但没有数据行")
                    return False

                month_data = []
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 4:
                        date = cols[0].text.strip()
                        weather = cols[1].text.strip()
                        temp = cols[2].text.strip()
                        wind = cols[3].text.strip()

                        month_data.append([date, weather, temp, wind])

                if month_data:
                    self.all_data.extend(month_data)
                    print(f"成功获取 {year}年{month}月 数据，共 {len(month_data)} 条记录")
                    return True
                else:
                    print(f"警告: 在 {url} 中未找到有效天气数据")
                    return False

            except requests.RequestException as e:
                print(f"请求异常 (尝试 {attempt + 1}/{self.max_attempts}): {e}")
                if attempt == self.max_attempts - 1:
                    print(f"错误: 达到最大重试次数，跳过 {year}年{month}月")
                    return False
                time.sleep(5)  # 重试前等待更长时间
            except Exception as e:
                print(f"处理异常 (尝试 {attempt + 1}/{self.max_attempts}): {e}")
                if attempt == self.max_attempts - 1:
                    print(f"错误: 达到最大重试次数，跳过 {year}年{month}月")
                    return False
                time.sleep(5)

        return False

    def run(self):
        """运行爬虫主程序，增加数据验证和结果保存"""
        print("开始爬取大连市近三年天气数据...")

        # 获取当前年份和月份
        current_year = time.localtime().tm_year
        current_month = time.localtime().tm_mon

        # 计算前三年加今年的年份范围
        years = list(range(current_year - 3, current_year + 1))
        # years = [2022, 2023, 2024，2025]

        # 记录成功和失败的月份
        success_months = 0
        failed_months = 0

        # 遍历每个月
        for year in years:
            # 对于当前年份，只爬取到当前月份
            end_month = current_month if year == current_year else 12

            for month in range(1, end_month + 1):
                success = self.fetch_weather(year, month)
                if success:
                    success_months += 1
                else:
                    failed_months += 1

        # 输出爬取总结
        print("\n===== 爬取总结 =====")
        print(f"成功获取 {success_months} 个月份的数据")
        print(f"失败 {failed_months} 个月份的数据")
        print(f"总共获取了 {len(self.all_data)} 条天气记录")

        # 检查是否有数据
        if not self.all_data:
            print("错误: 未获取到任何天气数据，程序终止")
            return

        # 处理数据
        print("正在处理数据...")
        columns = ['date', 'weather', 'temperature', 'wind']
        df = pd.DataFrame(self.all_data, columns=columns)

        # 提取温度数据
        df[['max_temperature', 'min_temperature']] = df['temperature'].str.extract(r'(\d+|\-?\d+)℃ \/ (\d+|\-?\d+)℃')

        # 处理可能提取失败的情况
        df['max_temperature'] = pd.to_numeric(df['max_temperature'], errors='coerce')
        df['min_temperature'] = pd.to_numeric(df['min_temperature'], errors='coerce')

        # 提取风力数据
        df[['wind_day', 'wind_night']] = df['wind'].str.extract(r'(.*) \/ (.*)')

        # 保存数据
        output_path = os.path.join(self.data_dir, 'dalian_weather_data.csv')
        df.to_csv(output_path, index=False, encoding='utf-8-sig')

        print(f"\n数据已成功保存到: {output_path}")
        print(f"数据包含 {len(df)} 行，{len(df.columns)} 列")
        print("数据前几行预览:")
        print(df.head().to_string())


if __name__ == "__main__":
    spider = WeatherSpider()
    spider.run()