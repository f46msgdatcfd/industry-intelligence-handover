# 📦 01_data_scraping

This directory contains the full pipeline for structured batch search and data collection using:

- Google Custom Search API (GCS)
- SerpAPI Web search
- SerpAPI News vertical

Each module is fully documented and supports batch scraping, intermediate merging, and final result consolidation.

---

## 🗂️ Directory Structure & Responsibilities

| Folder | Description |
|--------|-------------|
| `01_gcs_google_search_batch/` | Uses Google CSE API to perform structured batch search (GCS) |
| `02_serp_google_search_batch/01_web_search/` | Uses SerpAPI to scrape web search results |
| `02_serp_google_search_batch/02_news_search/` | Uses SerpAPI to fetch news headlines |
| `03_combine_results/` | Merges results from all modules into a unified final file |
| `configs/` | Contains shared config templates for GCS and SerpAPI API keys |

---

## 🚀 How to Run Manually

### 📦 Install Dependencies

Before running any script, please install required packages:

```bash
pip install -r requirements.txt
```

Make sure you are using a virtual environment or conda environment if needed.

This project uses the official SerpAPI SDK:

```bash
pip install google-search-results
```

⚠️ **Do NOT install `serpapi` – it's incorrect and unrelated.**

---

### GCS search:

```bash
cd 01_gcs_google_search_batch
python batch_search_main.py
python merge_all_csv.py
```

### SerpAPI Web:

```bash
cd ../02_serp_google_search_batch/01_web_search
python run_web_search.py
python merge_serp_web_csvs.py
```

### SerpAPI News:

```bash
cd ../02_news_search
python run_news_search.py
python merge_news_csv.py
```

### Merge All:

```bash
cd ../../../03_combine_results
cp ../01_gcs_google_search_batch/*.csv .
cp ../02_serp_google_search_batch/01_web_search/*.csv .
cp ../02_serp_google_search_batch/02_news_search/*.csv .
python merge_csv_results.py
```

---

## ⚡ One-Click Execution

You can also run the entire workflow by executing the batch script:

```bash
bash run_all.sh
```

It will:
- Run all batch scraping jobs
- Merge individual module results
- Copy merged files into the final folder
- Produce one file: `combined_results_YYYYMMDD_HHMMSS.csv`

---

## 🔐 Configs

Create your `gcs_config.py` and `serpapi_config.py` in the `configs/` folder using the provided templates.

```python
# configs/gcs_config.py
API_KEY = "your_google_api_key"
SEARCH_ENGINE_ID = "your_search_engine_id"

# configs/serpapi_config.py
SERP_API_KEY = "your_serpapi_key"
```