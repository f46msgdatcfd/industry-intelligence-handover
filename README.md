# 🧠 INDUSTRY-INTELLIGENCE-HANDOVER

本项目旨在实现一套面向行业情报的自动化数据处理系统，涵盖以下五个模块：

1. 数据抓取（已完成）
2. 数据清洗与预处理（部分完成）
3. 数据存储（结构预留）
4. 大模型分类与抽取（结构预留）
5. 前端可视化输出接口（结构预留）

---

## ✅ 已完成模块概览

### `01_data_scraping`

- 功能：通过 Google Custom Search API、requests 和 Playwright 批量抓取新闻网页内容。
- 特性：
  - 多参数组合搜索（关键词、地区、语言、时间段）
  - 自动切分日期区间（如按年/季度）
  - 搜索结果结构化输出（JSON/CSV/Excel）
  - 支持搜索失败重试及异常链接二次爬取
- 技术栈：Python, requests, Playwright, pandas

### `02_data_processing/clean_news.py`

- 功能：读取抓取结果，对新闻正文进行结构化提取。
- 状态：已完成清洗与文本抽取部分，计划后续接入大模型处理。

---

## 📂 项目结构概览

```
├── 01_data_scraping/         # 搜索与爬虫相关模块（已完成）
├── 02_data_processing/       # 数据清洗与初步分类（部分完成）
├── 03_data_storage/          # 数据库存储模块（预留）
├── 04_llm_usecases/          # 大模型分类与抽取用例（预留）
├── 05_output_interface/      # 可视化前端模块（预留）
├── project_index.md          # 项目索引（结构化总览）
├── README.md                 # 项目说明文档（当前文件）
├── structure_log.md          # 文件结构变更记录
```

---

## 🛠️ 环境与依赖安装

建议使用 [conda](https://docs.conda.io/) 管理环境：

```bash
conda create -n industry_intel python=3.10
conda activate industry_intel
pip install -r requirements.txt
```

如需运行 Playwright 抓取模块，请执行：

```bash
playwright install
```

---

## 🚀 运行示例

运行数据抓取模块（伪代码示例）：

```bash
python run_news_search.py --brand "tiomarkets" --location "us" --from "2019-01-01" --to "2020-01-01"
```

运行清洗模块：

```bash
python clean_news.py --input raw_news.json --output cleaned_news.csv
```

---

## 📌 注意事项

- 本项目结构设计完整，但非所有模块已开发完毕。
- 所有已完成模块均配有测试样例，具体见 `test_llm_classification.py`。
- 大模型接口接入相关代码已预留（见 `llm_utils.py`），但未正式启用。

---

## 📇 作者信息

- 作者：Winter Hu
- 最后更新：2025年4月25日