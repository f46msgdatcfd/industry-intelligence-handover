# 🔗 Combine Search Results (GCS + SerpAPI + News)

This module consolidates all output CSV files from the three submodules:

- `gcs_google_search_batch`
- `serp_google_search_batch/web_search`
- `serp_google_search_batch/news_search`

It produces a **deduplicated, standardized CSV** for downstream processing.

---

## 🚀 How to Run

### ✅ Step 1: Copy CSV files from each submodule

From the root of `01_data_scraping`, run:

```bash
cp gcs_google_search_batch/*.csv combine_results/
cp serp_google_search_batch/web_search/*.csv combine_results/
cp serp_google_search_batch/news_search/*.csv combine_results/
```

You should now have a folder like this:

```
combine_results/
├── merge_csv_results.py
├── search_*.csv
├── serp_api_*.csv
├── news_structured_*.csv
```

---

### ▶️ Step 2: Run the merge script

```bash
python merge_csv_results.py
```

The output will be saved with an auto-generated filename like:

```
combined_results_20250422_115422.csv
```

---

## 📊 Unified Output Schema

| Column | Description |
|--------|-------------|
| `title` | Title of the page/news |
| `url` | URL of the result |
| `snippet` | Short excerpt if available |
| `source_type` | One of `gcs`, `web`, or `news` |
| `source_file` | Which file this row originated from |

---

## 💡 Notes

- This script works only on **flat files in this folder**.
- It does **not scan subfolders**.
- Make sure to copy only files you want to include in the final merged result.