import requests
from bs4 import BeautifulSoup
import time
import random
import os
import json
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def create_session():
    session = requests.Session()
    retry = Retry(
        total=5,  # 重试次数
        backoff_factor=1,  # 每次失败后的等待时间 = backoff_factor * (2 ^ (重试次数 - 1))
        status_forcelist=[429, 500, 502, 503, 504],
        raise_on_status=False
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    })
    return session

def fetch_html(session, url):
    # 获取网页内容
    try:
        response = session.get(url, timeout=20)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"[Error] Request failed: {url}\n{e}")
        return None

def parse_dblp_papers(html):
    # 解析 DBLP 页面中的论文信息
    soup = BeautifulSoup(html, 'html.parser')
    papers = []
    for li in soup.find_all('li', class_='entry'):
        title_tag = li.find('span', class_='title')
        if not title_tag:
            continue
        title = title_tag.text.strip()
        authors = [a.text for a in li.find_all('span', itemprop='author')]
        papers.append({
            'title': title,
            'authors': authors
        })
    return papers

def crawl_conference(conference, years, save_path='data'):
    # 主爬虫逻辑
    os.makedirs(save_path, exist_ok=True)
    session = create_session()

    for year in years:
        print(f"Start crawling: {conference} {year}")
        filename = f"{save_path}/{conference}_{year}.json"
        if os.path.exists(filename):
            print(f"[Skip] Already exists: {filename}")
            continue

        url = f"https://dblp.org/db/conf/{conference.lower()}/{conference.lower()}{year}.html"
        html = fetch_html(session, url)
        if html is None:
            continue

        papers = parse_dblp_papers(html)
        print(f"[Done] {conference} {year}: {len(papers)} papers")
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(papers, f, ensure_ascii=False, indent=2)

        # 防止被封，加随机延迟
        time.sleep(random.uniform(3.0, 6.0))

if __name__ == '__main__':
    # 爬取 AAAI、ICML、CVPR、ICLR、IJCAI 2020至今的论文
    conference_years = {
        'aaai': [2020, 2021, 2022, 2023, 2024, 2025],
        'icml': [2020, 2021, 2022, 2023, 2024],  # 2025还未举办
        'cvpr': [2020, 2021, 2022, 2023, 2024],   # CVPR 2025 的条目尚未发布到 DBLP
        'iclr': [2020, 2021, 2022, 2023, 2024, 2025],
        'ijcai': [2020, 2021, 2022, 2023, 2024],    # 2025还未举办
    }

    for conf, years in conference_years.items():
        crawl_conference(conf, years)
