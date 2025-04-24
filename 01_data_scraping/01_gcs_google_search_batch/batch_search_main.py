from mi_google_search import google_search_all_results
import time
import numpy as np
from datetime import datetime, timedelta


# 构建2组笛卡尔积，进行批量搜索  batch search by build two catesian product
brand_list = ['oanda', 'tiomarkets']
region_list = ['us', 'canada']

# 映射 region 到 user_location
def resolve_location(region):
    region = region.lower()
    # the first group: us
    if region in ['us', 'the united states', 'america', 'american']:
        return 'us'
    # the second group: ca
    elif region in ['canada', 'canadian']:
        return 'ca'
    elif region == 'null':
        return None
    else:
        return None

# 构建每年一段的时间窗口 build a group for each year
year_ranges = [(f"{year}0101", f"{year+1}0101") for year in range(2024, 2026)]

# 构建并执行搜索任务 the final search task built
for brand in brand_list:
    for start_date, end_date in year_ranges:
        search_terms = brand
        start_date = start_date
        end_date = end_date
        filename = f"{brand}_{start_date}_{end_date}.csv".replace(" ", "_")
        print(f"🔍 查询中: {search_terms} [{start_date} ~ {end_date}]")
        try:
            google_search_all_results(
                search_terms=search_terms,
                start_date=start_date,
                end_date=end_date,
                csv_filename=filename
            )
            time.sleep(1)  # 防止速率限制 in case of the potential limiatations
        except Exception as e:
            print(f"❌ 查询失败: {filename} | 错误: {e}")

    
        for region in region_list:
            user_location = resolve_location(region)
            search_terms = f"{brand} {region}" if region != 'null' else brand
            filename = f"{brand}_{region}_{user_location}_{start_date}_{end_date}.csv".replace(" ", "_")
            search_terms=search_terms
            user_location=user_location
            start_date=start_date
            end_date=end_date
            csv_filename=filename
            print(f"🔍 查询中: {search_terms} [{start_date} ~ {end_date}], user_location={user_location}")
            try:
                google_search_all_results(
                    search_terms=search_terms,
                    user_location=user_location,
                    start_date=start_date,
                    end_date=end_date,
                    csv_filename=filename
                )
                time.sleep(1)  # 防止速率限制
            except Exception as e:
                print(f"❌ 查询失败: {filename} | 错误: {e}")