# prompt_loader.py
from pathlib import Path

def load_prompt(name: str) -> str:
    """
    加载指定名称的 prompt 文本（纯文本，无变量名）。
    默认从 prompts/ 目录下读取对应 .txt 文件。
    """
    prompt_path = Path(__file__).parent / "prompts" / f"{name}.txt"
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")

    with open(prompt_path, "r", encoding="utf-8") as f:
        text = f.read()
        print(f"🔍 [DEBUG] Loaded prompt '{name}': {len(text)} chars\n{text[:200]}...")
        return text