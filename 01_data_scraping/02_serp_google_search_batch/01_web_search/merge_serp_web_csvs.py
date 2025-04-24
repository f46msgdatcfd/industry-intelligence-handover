import pandas as pd
import os
import glob

def merge_serp_web_csvs(output_filename="merged_serp_web_results.csv"):
    """
    在 output 文件夹中合并所有以 serp_api_ 开头的 CSV 文件，并输出合并结果。
    每条记录添加 source_file 字段记录来源。
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    csv_files = glob.glob(os.path.join(output_dir, "serp_api_*.csv"))

    if not csv_files:
        print("⚠️ 没有找到以 serp_api_ 开头的 CSV 文件。")
        return

    dfs = []
    for filepath in csv_files:
        try:
            df = pd.read_csv(filepath)
            df["source_file"] = os.path.basename(filepath)
            dfs.append(df)
        except Exception as e:
            print(f"❌ 无法读取文件 {filepath}: {e}")

    if not dfs:
        print("⚠️ 没有成功读取任何文件。")
        return

    merged_df = pd.concat(dfs, ignore_index=True)
    output_path = os.path.join(output_dir, output_filename)
    merged_df.to_csv(output_path, index=False, encoding="utf-8-sig")

    print(f"✅ 合并完成，共 {len(merged_df)} 条记录，保存至: {output_path}")

if __name__ == "__main__":
    merge_serp_web_csvs()
