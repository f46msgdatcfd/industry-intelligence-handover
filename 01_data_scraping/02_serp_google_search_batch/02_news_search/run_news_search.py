import json
from serpapi import GoogleSearch
import pandas as pd
import os 

try:
    from configs.serpapi_config import SERP_API_KEY
except ImportError:
    raise Exception("Please create a config.py file with your SERP_API_KEY")

class GoogleNewsAPI:
    def __init__(self, query, start_date, end_date, api_key=None,
                 language="en", google_domain="google.ca", gl="ca",
                 engine="google", lr=None):
        self.query = query
        self.start_date = start_date
        self.end_date = end_date
        self.api_key = api_key
        self.language = language
        self.google_domain = google_domain
        self.gl = gl
        self.engine = engine
        self.lr = lr

        self.base_params = {
            "engine": self.engine,
            "q": self.query,
            "google_domain": self.google_domain,
            "gl": self.gl,
            "hl": self.language,
            "tbm": "nws",
            "tbs": f"cdr:1,cd_min:{self.start_date},cd_max:{self.end_date}",
            "api_key": self.api_key
        }

        if self.lr is not None:
            self.base_params["lr"] = self.lr

        self.results = []
        self.full_results = []
        self.page = 0

        if not self.api_key:
            raise ValueError("必须提供有效的 SerpApi 'api_key' 参数")

    def fetch_data(self):
        while True:
            self.base_params["start"] = self.page * 10
            search = GoogleSearch(self.base_params)
            results = search.get_dict()
            self.full_results.append(results)
            self.results.extend(results.get("news_results", []))
            next_page = results.get("pagination", {}).get("next")
            if next_page is None:
                print("所有数据已拉取完毕")
                break
            else:
                print(f"正在拉取第 {self.page + 1} 页数据...")
                self.page += 1

    def save_to_json(self, file_path):
        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(self.full_results, json_file, indent=4, ensure_ascii=False)
        print(f"完整数据已保存到 {file_path}")

    def load_from_json(self, file_path):
        with open(file_path, "r", encoding="utf-8") as json_file:
            self.full_results = json.load(json_file)
            self.results = []
            for page in self.full_results:
                self.results.extend(page.get("news_results", []))
        return self.full_results

    def news_to_csv(self, csv_file_path):
        if not self.results:
            raise ValueError("没有可用的新闻数据，请先调用 fetch_data() 或 load_from_json()")
        fields = ['position', 'link', 'title', 'source', 'date', 'snippet', 'thumbnail']
        news_list = [{field: news.get(field, None) for field in fields} for news in self.results]
        df = pd.DataFrame(news_list, columns=fields)
        df.to_csv(csv_file_path, index=False, encoding="utf-8-sig")
        print(f"✅ 新闻数据已成功写入 CSV 文件：{csv_file_path}")

# 示例用法（手动运行）
if __name__ == "__main__":
    queries = ["OANDA", "TioMarkets"]
    date_ranges = [("01/01/2024", "01/31/2024"), ("02/01/2024", "02/28/2024")]

    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    for q in queries:
        for start_date, end_date in date_ranges:
            print(f"📡 正在处理: {q} | 日期区间: {start_date} ~ {end_date}")
            client = GoogleNewsAPI(
                query=q,
                start_date=start_date,
                end_date=end_date,
                api_key=SERP_API_KEY,
                google_domain="google.com",
                gl="sg",
                language="en"
            )
            client.fetch_data()

            slug = q.replace(" ", "_")
            start_safe = start_date.replace("/", "-")
            end_safe = end_date.replace("/", "-")

            json_file = os.path.join(output_dir, f"news_raw_{slug}_{start_safe}_{end_safe}.json")
            csv_file = os.path.join(output_dir, f"news_structured_{slug}_{start_safe}_{end_safe}.csv")

            client.save_to_json(json_file)

            try:
                client.news_to_csv(csv_file)
            except ValueError:
                print(f"⚠️ 无新闻数据，跳过 CSV 写入: {q} [{start_safe} ~ {end_safe}]")
                continue
