# llm_utils.py
# 使用 DeepSeek 原生 API 判断网页内容是否有价值，结构化输出 valuable / useless

import re
import json
import requests
from urllib.parse import urlparse
from config import LLM_ENABLED, LLM_API_KEY, LLM_PROVIDER, LLM_TRIGGER_DOMAINS, LLM_WORD_LIMIT
from prompt_loader import load_prompt

# ========== mock 判别逻辑（无需调用模型） ==========
def mock_llm_classify(text: str) -> str:
    keywords = ["blockchain", "bitcoin", "forex", "token", "crypto", "web3", "cfd", "prop"]
    return "valuable" if any(k in text.lower() for k in keywords) else "useless"

# ========== 判断是否启用 LLM 判断 ==========
def should_use_llm(domain: str) -> bool:
    return LLM_ENABLED and domain in LLM_TRIGGER_DOMAINS

# ========== 调用 DeepSeek 原生 JSON API 实现结构化分类 ==========
def real_llm_classify(text: str, provider: str, api_key: str) -> str:
    if provider == "deepseek":
        prompt = load_prompt("antibot_classification").replace("{text}", text[:LLM_WORD_LIMIT * 6])
        try:
            response = requests.post(
                url="https://api.deepseek.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}"},
                json={
                    "model": "deepseek-chat",
                    "response_format": { "type": "json_object" },
                    "temperature": 0.0,
                    "max_tokens": 256,
                    "messages": [{"role": "user", "content": prompt}]
                },
                timeout=15
            )
            parsed = response.json()
            content = parsed.get("choices", [{}])[0].get("message", {}).get("content", "")
            result = json.loads(content.strip())
            return result.get("classification", "unknown")
        except Exception as e:
            return f"error: {e.__class__.__name__}"
    else:
        return mock_llm_classify(text)

# ========== 主函数：决定是否启用、调用模型，返回结构化分类结果 ==========
def evaluate_content_with_llm(url: str, content: str, max_words: int = LLM_WORD_LIMIT) -> tuple[str, str]:
    """
    判断网页内容是否有价值。
    返回一个二元组：(llm_classification, filtered_content)
    """
    domain = urlparse(url).netloc.replace("www.", "")
    short_text = " ".join(content.split()[:max_words])

    trigger_keywords = [
        "sign up", "cookie policy", "enable javascript", "subscribe",
        "terms of service", "quote delay", "support team", "opens new tab",
        "all rights reserved", "access unmatched financial data"
    ]

    should_trigger = (
        LLM_ENABLED and (
            domain in LLM_TRIGGER_DOMAINS
            or len(content) < 300
            or any(k in content.lower() for k in trigger_keywords)
        )
    )

    if not should_trigger:
        return "not_used", content

    result = real_llm_classify(short_text, provider=LLM_PROVIDER, api_key=LLM_API_KEY)
    return result, content if result == "valuable" else None