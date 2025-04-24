#!/bin/bash

echo "🚀 Starting full scraping + merging workflow..."
export PYTHONPATH=$(pwd)
cd "$(dirname "$0")" || exit 1

# Step 1: Run GCS search + merge
echo "🔍 Running GCS batch search..."
python 01_gcs_google_search_batch/batch_search_main.py

echo "🔗 Merging GCS results..."
python 01_gcs_google_search_batch/merge_all_csv.py

# Step 2: Run SerpAPI Web search + merge
echo "🔍 Running SerpAPI Web search..."
python 02_serp_google_search_batch/01_web_search/run_web_search.py

echo "🔗 Merging SerpAPI Web results..."
python 02_serp_google_search_batch/01_web_search/merge_serp_web_csvs.py

# Step 3: Run SerpAPI News search + merge
echo "📰 Running SerpAPI News search..."
python 02_serp_google_search_batch/02_news_search/run_news_search.py

echo "🔗 Merging SerpAPI News results..."
python 02_serp_google_search_batch/02_news_search/merge_news_csv.py

echo "🧹 Cleaning previous merged outputs..."
rm -f 03_combine_results/output/*.csv
rm -f 03_combine_results/merged_*.csv


# Step 4: Copy merged CSVs into combine_results/
echo "📁 Copying merged CSVs into combine_results/..."
cp 01_gcs_google_search_batch/output/merged_*.csv 03_combine_results/output/
cp 02_serp_google_search_batch/01_web_search/output/merged_*.csv 03_combine_results/output/
cp 02_serp_google_search_batch/02_news_search/output/merged_*.csv 03_combine_results/output/

# Step 5: Run final merge
echo "🔄 Running final cross-module merge..."
python 03_combine_results/merge_csv_results.py

echo "✅ All done!"
