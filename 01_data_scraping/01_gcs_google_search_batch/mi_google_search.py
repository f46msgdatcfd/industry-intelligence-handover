# mi_google_search.py

import requests
import time
import csv
import os 


try:
    from configs.gcs_config import API_KEY, SEARCH_ENGINE_ID
except ImportError:
    raise Exception("Please create a config.py file with your API_KEY and SEARCH_ENGINE_ID")

# Optional: use the keys below for local testing ONLY if you don't want to configure `config.py` yet.
# ⚠️ These keys may expire or be removed. Replace with your own in production.
#API_KEY = "AIzaSyC3WJ7PJMCW3Iw-k438QMCJEAT-Auqn_Uc"
#SEARCH_ENGINE_ID = "c1a4d01d1f3eb4c6b"
#SEARCH_ENGINE_ID = "55b659f2f13444b3e"


def google_search_all_results(
    search_terms,
    mustinclude_terms=None,
    ui_language=None,
    content_language=None,
    exclude_terms=None,
    or_terms=None,
    start_date=None,
    end_date=None,
    server_country=None,
    user_location=None,
    max_results=100,
    csv_filename=None
):
    """
    Fetch up to 100 search results (titles & URLs) from Google Custom Search API and save to CSV.

    Args:
        search_terms (str): The primary search query terms.
        mustinclude_terms (str, optional): Terms that must be included in results.
        ui_language (str, optional): User interface language (e.g., 'en', 'zh-CN').
        content_language (str, optional): Language of the documents (e.g., 'lang_en').
        exclude_terms (str, optional): Terms to exclude from results.
        or_terms (str, optional): Terms where at least one must appear in results.
        start_date (str, optional): Start date for results (format: YYYYMMDD).
        end_date (str, optional): End date for results (format: YYYYMMDD).
        server_country (str, optional): Restrict results to a country (e.g., 'countryUS').
        user_location (str, optional): Boost results based on user location (e.g., 'us').
        max_results (int, optional): Maximum number of results to return (max 100).
        csv_filename (str, optional): Filename for CSV output. If None, auto-generates based on search terms.

    Returns:
        list: A list of tuples containing (title, link) for each search result.
    """
    all_results = []
    results_per_page = 10  # API returns max 10 results per request
    start_index = 1  # Google uses 1-based indexing
    filter_dup = "1"  # Turn on duplicate content filter

    # Ensure max_results doesn't exceed API limit of 100
    max_results = min(max_results, 100)

    while len(all_results) < max_results:
        url = (
            f"https://www.googleapis.com/customsearch/v1?q={search_terms}"
            f"&key={API_KEY}&cx={SEARCH_ENGINE_ID}"
            f"&filter={filter_dup}"
            f"{f'&gl={user_location}' if user_location else ''}"
            f"{f'&cr={server_country}' if server_country else ''}"
            f"{f'&exactTerms={mustinclude_terms}' if mustinclude_terms else ''}"
            f"{f'&excludeTerms={exclude_terms}' if exclude_terms else ''}"
            f"{f'&orTerms={or_terms}' if or_terms else ''}"
            f"{f'&sort=date:r:{start_date}:{end_date}' if start_date and end_date else ''}"
            f"{f'&hl={ui_language}' if ui_language else ''}"
            f"{f'&lr={content_language}' if content_language else ''}"
            f"&start={start_index}&num={results_per_page}"
        )

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes
            data = response.json()

            if "items" not in data:
                print("No more results available or API limit reached.")
                break

            for item in data["items"]:
                title = item.get("title", "No title available")
                link = item.get("link", "No link available")
                snippet = item.get("snippet","No Snippet available")
                all_results.append((title, link, snippet))
                #print(f"{len(all_results)}. {title} - {link}")

                if len(all_results) >= max_results:
                    break

            start_index += results_per_page

            if start_index > 91:
                break

            time.sleep(1)  # Avoid hitting API rate limits

        except requests.exceptions.RequestException as e:
            print(f"Error fetching results: {e}")
            break

    results = all_results[:max_results]  # Ensure we don't return more than requested

    # Generate default CSV filename if not provided
    if csv_filename is None:
        csv_filename = f"search_results_{user_location}_{content_language}_{search_terms.replace(' ', '_')}.csv"
    # Save results to a CSV file in the same folder as this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir,"output")
    os.makedirs(output_dir,exist_ok=True)

    csv_path = os.path.join(output_dir, csv_filename)

    # Save results to a CSV file
    with open(csv_path, "a", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        # Write header only if file is empty/new
        if file.tell() == 0:
            writer.writerow(["Title", "URL","Snippet"])
        writer.writerows(results)

    print(f"\n✅ Retrieved {len(results)} results for '{search_terms}'")
    print(f"📁 Saved to: {csv_path}")

    return results

if __name__ == "__main__":
    # Example usage when running the script directly
    results = google_search_all_results(
        search_terms="best cfd broker in canada",
        mustinclude_terms="Oanda",
        ui_language="fr",
        user_location="ca",
        max_results=100,
        csv_filename="best_cfd_broker_in_canada_onada_global_fr_frc_frui.csv"
    )
