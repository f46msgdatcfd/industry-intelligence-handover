import pandas as pd
import glob
import os

def merge_csv_files_pandas(output_filename="merged_search_results.csv"):
    """
    使用 Pandas 合并当前脚本目录下所有 CSV 文件，并根据 URL 去重。
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir,"output")
    os.makedirs(output_dir,exist_ok=True)

    csv_path = os.path.join(output_dir, output_filename)

    csv_files = glob.glob(os.path.join(output_dir, "*.csv"))
    csv_files = [f for f in csv_files if os.path.basename(f) != output_filename]

    if not csv_files:
        print("⚠️ No CSV files found in the script directory.")
        return

    df_all = []

    for file in csv_files:
        try:
            df = pd.read_csv(file, encoding="utf-8-sig")
            expected_cols = ["Title", "URL", "Snippet"]
            if list(df.columns)[:3] != expected_cols:
                print(f"⚠️ {file} does not match expected columns. Skipping.")
                continue
            df["SourceFile"] = os.path.splitext(os.path.basename(file))[0]
            df_all.append(df)
        except Exception as e:
            print(f"❌ Failed to read {file}: {e}")
            continue

    if not df_all:
        print("⚠️ No valid CSV files to merge.")
        return

    df_merged = pd.concat(df_all, ignore_index=True)
    df_merged = df_merged.drop_duplicates(subset="URL", keep="first")
    df_merged = df_merged.sort_values("Title")

    df_merged.to_csv(csv_path, index=False, encoding="utf-8-sig")
    print(f"✅ Merged {len(df_merged)} unique rows into {output_filename}.")
    print(df_merged.head(3))

if __name__ == "__main__":
    merge_csv_files_pandas()
