# 🌐 SerpAPI Web Search Module

This module performs structured web search using SerpAPI's `organic_results`.

---

## 🚀 How to Run

1. **Create `config.py` in this folder:**

📝 Edit `../configs/serpapi_config.py` to set your SerpAPI key.



2. **Install dependencies**:

```bash
pip install google-search-results pandas
```

> ⚠️ **Note:** The correct package name for SerpAPI is:
>
> ```bash
> pip install google-search-results
> ```
> 
> ❌ Do **not** use `pip install serpapi` – that is incorrect and unrelated.

3. **Run the script:**

```bash
python run_web_search.py
```

---

## 📊 Output

Each query will generate:

- A `.csv` file: `serp_api_{query}_{gl}.csv`
- A `.json` file: full raw SerpAPI response

---

## 🧩 Output Schema

| Field | Description |
|-------|-------------|
| `title` | Page title |
| `link` | Result URL |
| `snippet` | Text excerpt from the page |
| `redirect_link` | Redirected URL, if any |
| `displayed_link` | Shown link in result |
| `date` | Published date (if any) |
| `snippet_highlighted_words` | Highlighted terms |
| `search_param_q` | Original search query |
| `search_param_gl` | Target country code |

---

## 📁 File Naming

CSV files are named based on query and region:

```
serp_api_best_cfd_broker_in_USA_Oanda_sg.csv
```

Raw JSON files use:

```
serpapi_web_results_best_cfd_broker_in_USA_Oanda_sg.json
```