import requests
import time
import pandas as pd
from typing import List, Dict, Optional


class DataCollector:
    
    def __init__(self):
        self.base_url = "https://www.hurun.net/zh-CN/Rank/HsRankDetailsList"
        self.headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://www.hurun.net/zh-CN/Rank/HsRankDetails?pagetype=rich",
            "sec-ch-ua": "\"Not;A=Brand\";v=\"99\", \"Microsoft Edge\";v=\"139\", \"Chromium\";v=\"139\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0",
            "x-requested-with": "XMLHttpRequest"
        }
        self.cookies = {
            "__utma": "245691549.1711475637.1752046257.1752046257.1752046257.1",
            "__utmc": "245691549",
            "__utmz": "245691549.1752046257.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)",
            "__utmt": "1",
            "Hm_lvt_2b09927a5895e3946dc6de8526befc81": "1752046257",
            "HMACCOUNT": "7E7E2407C53C1BDE",
            "Hm_lpvt_2b09927a5895e3946dc6de8526befc81": "1752046421",
            "__utmb": "245691549.3.10.1752046257"
        }
        self.data = []
        
    def collect_page_data(self, offset: int = 0, limit: int = 20) -> Optional[Dict]:
        params = {
            "num": "ODBYW2BI",  # 固定参数
            "search": "",
            "offset": str(offset),
            "limit": str(limit)
        }
        
        try:
            response = requests.get(
                self.base_url, 
                headers=self.headers, 
                cookies=self.cookies, 
                params=params,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"数据采集失败: {e}")
            return None
    
    def collect_all_data(self, max_pages: int = 50) -> List[Dict]:
        offset = 0
        limit = 20
        page_count = 0
        
        while page_count < max_pages:
            page_data = self.collect_page_data(offset, limit)
            if not page_data or not page_data.get('rows'):
                break
                
            data_list = page_data['rows']
            if not data_list:
                break
                

            processed_data = []
            for item in data_list:
                processed_item = self._process_data_item(item)
                if processed_item:
                    processed_data.append(processed_item)
            
            self.data.extend(processed_data)
            print(f"已采集第 {page_count + 1} 页，累计 {len(self.data)} 条数据")
            

            if len(data_list) < limit:
                break
                
            offset += limit
            page_count += 1
            time.sleep(1)  # 防止请求过快
            
        print(f"数据采集完成，共采集 {len(self.data)} 条数据")
        return self.data
    
    def _process_data_item(self, item: Dict) -> Optional[Dict]:
        try:
            processed = {}
            

            processed['ranking'] = item.get('hs_Rank_Rich_Ranking', 0)
            processed['name'] = item.get('hs_Rank_Rich_ChaName_Cn', '未知')
            processed['wealth'] = item.get('hs_Rank_Rich_Wealth', 0)  # 财富值
            processed['wealth_change'] = item.get('hs_Rank_Rich_Wealth_Change', '0%')
            processed['ranking_change'] = item.get('hs_Rank_Rich_Ranking_Change', '0')
            

            processed['company'] = item.get('hs_Rank_Rich_ComName_Cn', '未知')
            processed['company_en'] = item.get('hs_Rank_Rich_ComName_En', '')
            processed['headquarters'] = item.get('hs_Rank_Rich_ComHeadquarters_Cn', '未知')
            processed['industry'] = item.get('hs_Rank_Rich_Industry_Cn', '未知')
            processed['industry_en'] = item.get('hs_Rank_Rich_Industry_En', '')
            

            processed['relations'] = item.get('hs_Rank_Rich_Relations', '未知')
            

            character_info = item.get('hs_Character', [])
            if character_info and len(character_info) > 0:
                char = character_info[0]
                
                processed['gender'] = char.get('hs_Character_Gender', '未知')
                processed['age'] = char.get('hs_Character_Age', '未知')
                processed['birthday'] = char.get('hs_Character_Birthday', '')
                processed['nationality'] = char.get('hs_Character_Nationality', '')
                processed['birth_place'] = char.get('hs_Character_BirthPlace_Cn', '未知')
                processed['permanent_place'] = char.get('hs_Character_Permanent_Cn', '未知')
                processed['education'] = char.get('hs_Character_Education_Cn', '未知')
                processed['school'] = char.get('hs_Character_School_Cn', '未知')
                processed['native_place'] = char.get('hs_Character_NativePlace_Cn', '未知')
            else:
                processed['gender'] = '未知'
                processed['age'] = '未知'
                processed['birthday'] = ''
                processed['nationality'] = ''
                processed['birth_place'] = '未知'
                processed['permanent_place'] = '未知'
                processed['education'] = '未知'
                processed['school'] = '未知'
                processed['native_place'] = '未知'
            
            return processed
            
        except Exception as e:
            print(f"处理数据项时出错: {e}")
            return None
    
    def save_to_csv(self, filename: str = "hurun_data.csv") -> None:
        if not self.data:
            print("没有数据可保存")
            return
            
        df = pd.DataFrame(self.data)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"数据已保存到 {filename}")
    
    def get_data_frame(self) -> pd.DataFrame:
        return pd.DataFrame(self.data) if self.data else pd.DataFrame() 