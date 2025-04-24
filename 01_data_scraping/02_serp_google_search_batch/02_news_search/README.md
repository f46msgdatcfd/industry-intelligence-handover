# 🗞️ SerpAPI News Search Module

This module uses SerpAPI's `tbm=nws` (News Vertical) to fetch structured news data.

---

## 🚀 How to Run

1. **Edit `../configs/serpapi_config.py` to set your SerpAPI key.


2. **Install dependencies:**

```bash
pip install google-search-results pandas
```

3. **Run the script:**

```bash
python run_news_search.py
```

---

## ✅ Example: Batch Search

The script now supports batch execution for multiple queries and date ranges.

```python
queries = ["OANDA Canada", "TioMarkets Canada"]
date_ranges = [("01/01/2024", "02/01/2024"), ("02/01/2024", "03/01/2024")]

for query in queries:
    for start, end in date_ranges:
        client = GoogleNewsAPI(query, start, end, api_key=SERP_API_KEY)
        client.fetch_data()

        slug = query.replace(" ", "_")
        client.save_to_json(f"news_raw_{slug}_{start}_{end}.json")
        client.news_to_csv(f"news_structured_{slug}_{start}_{end}.csv")
```

This will produce different `.json` and `.csv` files per combination.

---

## 📊 Output

Each run generates:

- A `.json` file: full SerpAPI news response
- A `.csv` file: structured news output

---

## 🧩 Output Schema

| Field | Description |
|-------|-------------|
| title | News title |
| link | News article URL |
| source | Publisher |
| date | Published date |
| snippet | Summary |
| thumbnail | Image if available |

---

## 📁 File Naming Convention

- JSON: `news_raw_{query}_{start}_{end}.json`
- CSV: `news_structured_{query}_{start}_{end}.csv`