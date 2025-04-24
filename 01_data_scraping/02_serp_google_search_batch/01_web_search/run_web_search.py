from serpapi import GoogleSearch
import json
import os
import pandas as pd
import re
from datetime import datetime
now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
try:
    from configs.serpapi_config import SERP_API_KEY
except ImportError:
    raise Exception("Please create a config.py file with your SERP_API_KEY")

def sanitize_filename(s):
    return re.sub(r'\W+', '_', s.strip())

def fetch_and_parse_serpapi_improved(
    query: str,
    gl: str,
    api_key: str,
    max_pages: int = 10,
    output_dir: str = "./",
    base_filename: str = "serpapi_web_results"
):
    all_pages = []
    all_results = []
    results_per_page = 10
    total_pages = max_pages

    for page in range(max_pages):
        if page >= total_pages:
            break

        print(f"📄 正在抓取第 {page+1} 页...")

        start = page * results_per_page
        params = {
            "engine": "google",
            "q": query,
            "gl": gl,
            "api_key": api_key,
            "start": start
        }

        search = GoogleSearch(params)
        try:
            data = search.get_dict()
        except Exception as e:
            print(f"❌ SERP API 请求失败：{e}")
            break

        if "organic_results" not in data or not data["organic_results"]:
            print(f"⚠️ 第 {page+1} 页无 organic_results，终止抓取。")
            break

        all_pages.append(data)

        search_params = data.get("search_parameters", {})
        for item in data["organic_results"]:
            result = {
                "position": item.get("position"),
                "title": item.get("title"),
                "link": item.get("link"),
                "redirect_link": item.get("redirect_link"),
                "displayed_link": item.get("displayed_link"),
                "snippet": item.get("snippet"),
                "snippet_highlighted_words": item.get("snippet_highlighted_words", []),
                "source": item.get("source"),
                "sitelinks": item.get("sitelinks"),
                "must_include": item.get("must_include"),
                "missing": item.get("missing"),
                "date": item.get("date"),
                "search_param_q": search_params.get("q", query),
                "search_param_google_domain": search_params.get("google_domain"),
                "search_param_gl": search_params.get("gl", gl),
                "search_param_device": search_params.get("device")
            }
            all_results.append(result)

        pagination = data.get("serpapi_pagination") or {}
        if page == 0 and "other_pages" in pagination:
            total_pages = min(len(pagination["other_pages"]) + 1, max_pages)
        if "next" not in pagination:
            print("✅ 当前页无 next，抓取完成。")
            break

    safe_query = sanitize_filename(query)
    safe_gl = sanitize_filename(gl)
    json_filename = f"{base_filename}_{safe_query}_{safe_gl}.json"
    csv_filename = f"serp_api_{safe_query}_{safe_gl}_{now_str}.csv"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir,"output")
    os.makedirs(output_dir,exist_ok=True)
    json_path = os.path.join(output_dir, json_filename)
    csv_path = os.path.join(output_dir, csv_filename)

    with open(json_path, "w", encoding="utf-8") as jf:
        json.dump(all_pages, jf, indent=2, ensure_ascii=False)

    df = pd.DataFrame(all_results)
    df.to_csv(csv_path, index=False)

    print(f"✅ 抓取完成，共 {len(all_pages)} 页")
    print(f"📦 JSON 保存到：{json_path}")
    print(f"📊 CSV 保存到：{csv_path}")

    return {
        "json_output_path": json_path,
        "csv_output_path": csv_path
    }


if __name__ == "__main__":
    broker_keywords = [
        "Oanda",
        "TioMarkets"
    ]

    for keyword in broker_keywords:
        fetch_and_parse_serpapi_improved(
            query=keyword,
            gl="sg",
            api_key=SERP_API_KEY,
            max_pages=2
        )