# test_llm_classification_verbose.py
# 带输入内容打印的版本：完整输出最终传给 LLM 的 prompt 文本

from llm_utils import real_llm_classify, load_prompt
from config import LLM_API_KEY, LLM_PROVIDER, LLM_WORD_LIMIT

# 示例文本（疑似反爬页面）
test_text = """
Sign uphere.
Reporting by Shilpa Jamkhandikar; Editing by Raju Gopalakrishnan
Our Standards:The Thomson Reuters Trust Principles., opens new tab
An overnight Russian combined missile and drone attack triggered fires, smashed buildings and buried residents under rubble in the Ukrainian capital Kyiv, killing nine people and injuring more than 70, Ukrainian officials said on Thursday.
Reuters, the news and media division of Thomson Reuters, is the world’s largest multimedia news provider, reaching billions of people worldwide every day. Reuters provides business, financial, national and international news to professionals via desktop terminals, the world's media organizations, industry events and directly to consumers.
Access unmatched financial data, news and content in a highly-customised workflow experience on desktop, web and mobile.
Browse an unrivalled portfolio of real-time and historical market data and insights from worldwide sources and experts.
Screen for heightened risk individual and entities globally to help uncover hidden risks in business relationships and human networks.
All quotes delayed a minimum of 15 minutes.See here for a complete list of exchanges and delays.
© 2025 Reuters.All rights reserved
"""

if __name__ == "__main__":
    print("🔍 Testing LLM classification on suspicious content...")
    text = " ".join(test_text.split()[:LLM_WORD_LIMIT])
    prompt = load_prompt("antibot_classification").replace("{text}", text)
    print("🧾 Full Prompt Sent to LLM:\n")
    print(prompt)

    result = real_llm_classify(text, provider=LLM_PROVIDER, api_key=LLM_API_KEY)
    print("\n✅ Classification:", result)