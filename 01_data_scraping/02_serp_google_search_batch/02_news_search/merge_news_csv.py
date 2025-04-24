import pandas as pd
import glob
import os

def merge_news_csvs(output_filename="merged_news_results.csv"):
    """
    合并 output 目录下所有以 news_structured_ 开头的 CSV 文件。
    要求字段包括：position, link, title, source, date, snippet, thumbnail。
    添加 source_file 字段记录原始文件名。
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_filename)

    csv_files = glob.glob(os.path.join(output_dir, "news_structured_*.csv"))
    csv_files = [f for f in csv_files if os.path.basename(f) != output_filename]

    if not csv_files:
        print("⚠️ No matching news CSV files found.")
        return

    df_all = []

    for file in csv_files:
        try:
            df = pd.read_csv(file, encoding="utf-8-sig")
            expected_cols = ["position", "link", "title", "source", "date", "snippet", "thumbnail"]
            if list(df.columns)[:7] != expected_cols:
                print(f"⚠️ {file} does not match expected columns. Skipping.")
                continue
            df["source_file"] = os.path.splitext(os.path.basename(file))[0]
            df_all.append(df)
        except Exception as e:
            print(f"❌ Failed to read {file}: {e}")
            continue

    if not df_all:
        print("⚠️ No valid CSV files to merge.")
        return

    df_merged = pd.concat(df_all, ignore_index=True)
    df_merged = df_merged.drop_duplicates()

    df_merged.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"✅ Merged {len(df_merged)} unique rows into: {output_path}")

if __name__ == "__main__":
    merge_news_csvs()
