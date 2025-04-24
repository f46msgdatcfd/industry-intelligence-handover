# 📊 INDUSTRY-INTELLIGENCE-HANDOVER 项目索引

本项目旨在构建一个面向行业资讯的自动采集、清洗与初步分类系统。项目结构已分模块设计，目前已完成以下部分：

## ✅ 已完成模块

### `01_data_scraping`
- 功能：从指定搜索源（如 Google CSE）自动化抓取网页新闻内容及元信息。
- 特点：支持关键词逻辑组合、时间区间切片、地区语言过滤、多参数搜索组合。
- 输出格式：支持 JSON、CSV、Excel。
- 技术栈：requests + Playwright 双层爬取策略，失败链接自动重试。

### `02_data_processing/clean_news.py`
- 功能：对抓取网页进行清洗，提取标题、正文、发布时间等信息。
- 当前完成：集成爬虫部分逻辑，清洗模块雏形已具备。

## 🕗 模块结构预留（未开发）
- `02_data_processing/llm_utils.py`：预期用于接入大模型进行内容分类。
- `03_data_storage`：预留结构，计划用于本地或远程数据库持久化。
- `04_llm_usecases`：计划存放与 LLM 相关的实际业务用例。
- `05_output_interface/streamlit_app`：预留 Streamlit 可视化展示接口。

## 📁 项目其他说明文档
- `README.md`: 项目介绍与依赖说明（建议完善）
- `structure_log.md`: 项目目录与文件结构变更日志
