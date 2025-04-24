# 🔍 Google Custom Search Batch Query Tool

This module performs automated, large-scale querying of Google Custom Search API across various brand names, user locations, and yearly time intervals.

It is a foundational component in the `01_data_scraping` stage of the industry intelligence data pipeline, focusing on retrieving news and article links from the web.

---

## 🧠 Module Features

- ✅ Cartesian combination of brand × region
- ✅ Year-by-year slicing (2010–2025)
- ✅ Optional location boost (`gl=us`, `gl=ca`, etc.)
- ✅ Saves result into clean `.csv` files
- ✅ Avoids API quota rate limits with delays

---

## 🗂️ File Structure

```bash
google_search_batch/
├── batch_search_main.py         # Master script for batch query orchestration
├── mi_google_search.py          # Core logic for Google Search API querying
```

---

## 🚀 How to Run

### 1. Edit `../configs/serpapi_config.py` to set your SerpAPI key.

```python
# Inside mi_google_search.py or config.py
API_KEY = "your_google_api_key"
SEARCH_ENGINE_ID = "your_custom_engine_id"
```

### 2. Install requirements (once):

```bash
pip install requests pandas
```

### 3. Run the batch script:

```bash
python batch_search_main.py
```

This will generate `.csv` files like:

```
oanda_us_20120101_20130101.csv
tiomarkets_canada_ca_20200101_20210101.csv
```

---

## 🧪 Example Use Case

This tool was used to retrieve thousands of news articles mentioning CFD brokers like OANDA and TioMarkets for downstream classification and labeling.

---

## 📁 Output Format

Each `.csv` contains:

| Title | URL | Snippet |
|-------|-----|---------|

---

## 📌 Notes

- Max 100 results per query due to API limits
- Uses `time.sleep(1)` to throttle requests
- Handles region-to-location mapping (`us`, `ca`)