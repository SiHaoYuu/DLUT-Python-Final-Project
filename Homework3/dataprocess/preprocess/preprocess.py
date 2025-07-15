import os
import json
import pandas as pd

def load_all_json(json_folder='D:/test/paper/dataprocess/oridata'):
    all_data = []
    for filename in os.listdir(json_folder):
        if not filename.endswith('.json'):
            continue

        filepath = os.path.join(json_folder, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            papers = json.load(f)
        basename = filename.replace('.json', '')
        conf, year = basename.split('_')
        year = int(year)

        for paper in papers:
            all_data.append({
                'conference': conf.upper(),
                'year': year,
                'title': paper.get('title', '').strip(),
                'authors': ', '.join(paper.get('authors', []))
            })

    return pd.DataFrame(all_data)

if __name__ == '__main__':
    df = load_all_json('D:/test/paper/dataprocess/oridata')
    df.drop_duplicates(subset=['title', 'year'], inplace=True)
    df.to_csv('D:/test/paper/dataprocess/preprocess/papers_cleaned.csv', index=False)
    print(f"已生成清洗后的 CSV：D:/test/paper/dataprocess/preprocess/papers_cleaned.csv")
