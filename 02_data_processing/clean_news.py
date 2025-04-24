import requests
import json
import pandas as pd
import re
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import dateparser
import time
import random
import logging
from pathlib import Path
from playwright.sync_api import sync_playwright
from llm_utils import evaluate_content_with_llm

FILE_PREFIX = "default"

def set_file_prefix(prefix: str):
    global FILE_PREFIX
    FILE_PREFIX = prefix
    Path(f"screenshots_{FILE_PREFIX}").mkdir(parents=True, exist_ok=True)
    Path(f"output_{FILE_PREFIX}").mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=f"output_{FILE_PREFIX}/failed_urls.log",
        level=logging.WARNING,
        format="%(asctime)s - %(message)s"
    )

def load_session_cookies(domain_keyword):
    cookie_file_map = {
        "linkedin.com": "linkedin_cookies.json",
        "facebook.com": "facebook_cookies.json",
        "instagram.com": "instagram_cookies.json",
        "x.com": "twitter_cookies.json",
        "twitter.com": "twitter_cookies.json"
    }
    for key, file in cookie_file_map.items():
        if key in domain_keyword:
            path = Path(file)
            if path.exists():
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        return json.load(f)
                except:
                    pass
    return []

def inject_cookies_if_needed(context, url):
    cookies = load_session_cookies(url)
    if cookies:
        try:
            context.add_cookies(cookies)
        except:
            pass

def get_screenshot_path(url):
    safe_name = re.sub(r'[^a-zA-Z0-9]', '_', url)[:50]
    return f"screenshots_{FILE_PREFIX}/{safe_name}.png"

class ExcelWriterHelper:
    MAX_CELL_LENGTH = 32767

    @staticmethod
    def clean_text(text):
        if not text:
            return ""
        return str(text).strip().replace("\u200b", "").replace("\u200e", "")

    @staticmethod
    def truncate_text(text):
        if not text:
            return ""
        return text if len(text) <= ExcelWriterHelper.MAX_CELL_LENGTH else text[:ExcelWriterHelper.MAX_CELL_LENGTH] + " [已截断]"

    @staticmethod
    def escape_excel_formula(text):
        if isinstance(text, str) and text.startswith(("=", "+", "-", "@")):
            return "'" + text
        return text

    @classmethod
    def preprocess_record(cls, record: dict) -> dict:
        return {
            k: cls.escape_excel_formula(cls.truncate_text(cls.clean_text(v)))
            for k, v in record.items()
        }

    @classmethod
    def write_to_excel(cls, records: list, filename: str):
        df = pd.DataFrame([cls.preprocess_record(r) for r in records])
        df.fillna("", inplace=True)
        df.to_excel(filename, index=False)
        print(f"✅ Excel 已保存：{filename}")



def extract_publish_date_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    meta_selectors = [
        {'name': 'pubdate'}, {'name': 'publishdate'}, {'name': 'date'},
        {'name': 'dc.date.issued'}, {'property': 'article:published_time'},
        {'property': 'og:pubdate'}, {'itemprop': 'datePublished'}
    ]
    for selector in meta_selectors:
        meta_tag = soup.find("meta", attrs=selector)
        if meta_tag and meta_tag.get("content"):
            parsed = dateparser.parse(meta_tag["content"])
            if parsed:
                return parsed.isoformat()
    time_tag = soup.find("time", attrs={"datetime": True})
    if time_tag:
        parsed = dateparser.parse(time_tag["datetime"])
        if parsed:
            return parsed.isoformat()
    for tag in soup.find_all(["div", "span", "p"], class_=re.compile(r"(date|meta|info|time)", re.I)):
        text = tag.get_text(separator=" ", strip=True)
        if "published" in text.lower():
            date_match = re.search(r"(?:published\\W*)?(\\w+ \\d{1,2}, \\d{4}[^\\n]*)", text, re.I)
            if date_match:
                parsed = dateparser.parse(date_match.group(1))
                if parsed:
                    return parsed.isoformat()
    return None

def extract_author(soup):
    meta = soup.find("meta", attrs={"name": "author"})
    return meta["content"].strip() if meta and meta.get("content") else None

def extract_title(soup):
    og_title = soup.find("meta", property="og:title")
    if og_title and og_title.get("content"):
        return og_title["content"].strip()
    return soup.title.get_text(strip=True) if soup.title else None

def detect_failure_reason(html: str, title: str, content: str) -> str:
    if not html:
        return "no response"
    if "cloudflare" in html.lower() or "captcha" in html.lower():
        return "blocked by Cloudflare / captcha"
    if title and re.search(r"404|not found|page not found", title, re.I):
        return "404 / page not found"
    if content and len(content) < 100:
        return "very short content"
    if content and "enable javascript" in content.lower():
        return "JS required / unsupported browser"
    if not content:
        return "no content"
    return "ok"

def is_anti_bot_page(html: str) -> bool:
    if not html:
        return True
    keywords = [
        "cloudflare", "captcha", "access denied", "enable javascript",
        "403 forbidden", "are you a robot", "please verify", "prove you are human"
    ]
    return any(k in html.lower() for k in keywords)

def requests_only_fetch(url: str) -> dict:
    from llm_utils import evaluate_content_with_llm

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com"
    }

    try:
        time.sleep(random.uniform(1, 2.5))
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200 and r.text.strip():
            soup = BeautifulSoup(r.text, "lxml")
            paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
            content_joined = "\n".join(paragraphs)

            # ✅ LLM 判断是否有价值
            llm_classification, filtered_content = evaluate_content_with_llm(url, content_joined)
            if not filtered_content:
                raise ValueError(f"LLM判定为无效内容 ({llm_classification})")

            return {
                "url": url,
                "content": filtered_content,
                "llm_classification": llm_classification,
                "publish_time": extract_publish_date_from_html(r.text),
                "title": extract_title(soup),
                "author": extract_author(soup),
                "scrape_time": datetime.now(timezone.utc).isoformat(),
                "method": "requests",
                "failed_reason": "ok",
                "screenshot": "",
                "has_screenshot": False
            }
    except Exception as e:
        logging.warning(f"[requests] Failed for {url}: {e.__class__.__name__} - {e}")

    return {
        "url": url,
        "content": None,
        "llm_classification": "failed",
        "publish_time": None,
        "title": None,
        "author": None,
        "scrape_time": datetime.now(timezone.utc).isoformat(),
        "method": "failed",
        "failed_reason": "blocked or failed request",
        "screenshot": "",
        "has_screenshot": False
    }



def playwright_only_fetch(url: str) -> dict:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }
    from llm_utils import evaluate_content_with_llm

    with sync_playwright() as p:
        browser = None
        page = None
        try:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent=headers["User-Agent"])
            inject_cookies_if_needed(context, url)
            page = context.new_page()
            page.goto(url, timeout=30000)
            page.wait_for_load_state("networkidle")

            content = page.content()
            llm_classification, filtered_content = evaluate_content_with_llm(url, content)

            soup = BeautifulSoup(content, "lxml")
            paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
            text_joined = "\n".join(paragraphs) if filtered_content else None

            return {
                "url": url,
                "content": text_joined,
                "llm_classification": llm_classification,
                "publish_time": extract_publish_date_from_html(content),
                "title": extract_title(soup),
                "author": extract_author(soup),
                "scrape_time": datetime.now(timezone.utc).isoformat(),
                "method": "playwright",
                "failed_reason": "ok" if filtered_content else f"blocked (LLM={llm_classification})",
                "screenshot": "",
                "has_screenshot": False
            }

        except Exception as e:
            screenshot_path = get_screenshot_path(url)
            if page:
                try:
                    page.screenshot(path=screenshot_path)
                    logging.warning(f"[playwright] Screenshot saved: {screenshot_path} | URL: {url}")
                    return {
                        "url": url,
                        "content": None,
                        "llm_classification": "unknown",
                        "publish_time": None,
                        "title": None,
                        "author": None,
                        "scrape_time": datetime.now(timezone.utc).isoformat(),
                        "method": "playwright",
                        "failed_reason": f"playwright exception: {e.__class__.__name__}",
                        "screenshot": screenshot_path,
                        "has_screenshot": True
                    }
                except:
                    pass
            return {
                "url": url,
                "content": None,
                "llm_classification": "unknown",
                "publish_time": None,
                "title": None,
                "author": None,
                "scrape_time": datetime.now(timezone.utc).isoformat(),
                "method": "playwright",
                "failed_reason": "playwright failed without screenshot",
                "screenshot": "",
                "has_screenshot": False
            }
        finally:
            if browser:
                browser.close()



def save_results(records: list, prefix: str):
    output_dir = Path(f"output_{FILE_PREFIX}")
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"{prefix}.json"
    excel_path = output_dir / f"{prefix}.xlsx"
    csv_path = output_dir / f"{prefix}.csv"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    ExcelWriterHelper.write_to_excel(records, str(excel_path))
    pd.DataFrame(records).to_csv(csv_path, index=False, encoding="utf-8-sig")

def scrape_multiple_urls(url_list, output_prefix="default"):
    set_file_prefix(output_prefix)
    primary, fallback = [], []
    failed_urls = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        for result in executor.map(requests_only_fetch, url_list):
            if result["method"] == "failed":
                failed_urls.append(result["url"])
            else:
                primary.append(result)
    save_results(primary, f"{output_prefix}_requests")
    with ThreadPoolExecutor(max_workers=2) as executor:
        for result in executor.map(playwright_only_fetch, failed_urls):
            fallback.append(result)
    all_results = primary + fallback
    save_results(all_results, f"{output_prefix}_final")
    return all_results

def scrape_from_excel(filepath: str, url_column: str = "url", prefix_override: str = None):
    df = pd.read_excel(filepath)
    if url_column not in df.columns:
        raise ValueError(f"列名 `{url_column}` 不存在于 Excel 中，当前列为：{list(df.columns)}")
    urls = df[url_column].dropna().tolist()
    if not urls:
        raise ValueError("Excel 中未找到有效 URL")
    filename = prefix_override or Path(filepath).stem
    return scrape_multiple_urls(urls, output_prefix=filename)



if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Batch scrape article content from URLs listed in an Excel file.")
    parser.add_argument("--input", required=True, help="Path to input Excel file with URLs.")
    parser.add_argument("--column", default="url", help="Column name in Excel that contains the URLs.")
    parser.add_argument("--prefix", default=None, help="Prefix for output files and folders.")

    args = parser.parse_args()

    print("🚀 启动抓取任务...")
    results = scrape_from_excel(filepath=args.input, url_column=args.column, prefix_override=args.prefix)
    print(f"🎯 共抓取成功 {len([r for r in results if r['content']])} 条，失败 {len([r for r in results if not r['content']])} 条。")