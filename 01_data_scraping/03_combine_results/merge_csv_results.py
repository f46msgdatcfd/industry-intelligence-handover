import pandas as pd
import os
from datetime import datetime
import glob

def merge_cross_module_csvs(output_prefix="combined_results"):
    """
    合并多个来源的搜索结果 CSV，标准化结构并添加来源字段。
    支持来源：
        - Web: 文件名以 "serp_api_" 开头
        - News: 文件名以 "news_structured_" 开头
        - GCS: 其它 CSV 文件（例如没有特定前缀的）
    
    输出文件名将包含时间戳，避免覆盖。
    """
    # 以当前脚本所在目录为基础目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"{output_prefix}_{now_str}.csv"
    output_path = os.path.join(output_dir, output_filename)
    
    csv_files = glob.glob(os.path.join(output_dir, "*.csv"))
    csv_files = [f for f in csv_files if os.path.basename(f) != output_filename]

    if not csv_files:
        print("⚠️ 没有可合并的 CSV 文件。")
        return

    merged_data = []

    for filepath in csv_files:
        filename = os.path.basename(filepath)
        try:
            df = pd.read_csv(filepath, encoding="utf-8-sig")

            # 来源判断
            if filename.startswith("serp_api_"):
                df = df.rename(columns={"link": "url"})
                required = ["title", "url", "snippet"]
                if all(col in df.columns for col in required):
                    df = df[required]
                df["source_type"] = "web"
            elif filename.startswith("news_structured_"):
                df = df.rename(columns={"link": "url"})
                if "title" in df.columns and "url" in df.columns:
                    if "snippet" not in df.columns:
                        df["snippet"] = ""
                    df = df[["title", "url", "snippet"]]
                df["source_type"] = "news"
            else:
                df = df.rename(columns={"Title": "title", "URL": "url", "Snippet": "snippet"})
                required = ["title", "url", "snippet"]
                if all(col in df.columns for col in required):
                    df = df[required]
                df["source_type"] = "gcs"

            df["source_file"] = filename
            merged_data.append(df)
        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")

    if merged_data:
        final_df = pd.concat(merged_data, ignore_index=True)
        final_df = final_df.drop_duplicates()
        final_df.to_csv(output_path, index=False, encoding="utf-8-sig")
        print(f"✅ 合并完成，共 {len(final_df)} 条记录，保存至: {output_path}")
        print("\n🔍 Preview:")
        print(final_df.head(3))
    else:
        print("⚠️ 没有可合并的 CSV 文件。")

if __name__ == "__main__":
    merge_cross_module_csvs()
