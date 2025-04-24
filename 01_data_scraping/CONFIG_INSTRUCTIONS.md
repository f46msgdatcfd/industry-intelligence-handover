# 🔐 Configuration Instructions

Before running this project, you must create two local configuration files in the `configs/` folder to supply your API credentials.

These files are excluded from version control via `.gitignore` and must be created manually using the provided templates.

---

## ✅ 1. Google Custom Search API

Create this file:

```
configs/gcs_config.py
```

Based on the template:

```
configs/gcs_config_template.py
```

```python
# gcs_config.py
API_KEY = "your_google_api_key"
SEARCH_ENGINE_ID = "your_search_engine_id"
```

---

## ✅ 2. SerpAPI Configuration

Create this file:

```
configs/serpapi_config.py
```

Based on the template:

```
configs/serpapi_config_template.py
```

```python
# serpapi_config.py
SERP_API_KEY = "your_serpapi_key"
```

---

## 📌 Notes

- These credentials are required for the following scripts:
  - `mi_google_search.py` (GCS)
  - `run_web_search.py` (SerpAPI Web)
  - `run_news_search.py` (SerpAPI News)

- Do not commit `gcs_config.py` or `serpapi_config.py` to version control. They are listed in `.gitignore`.

- Keep your keys secure. If deploying to a server or container, consider loading these via environment variables or Docker secrets.