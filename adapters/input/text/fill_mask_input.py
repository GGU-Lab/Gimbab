"""
📦 Input Adapter: fill_mask_input
──────────────────────────────────────────────
- 마스킹된 텍스트 입력을 받아 fill-mask 태스크용 구조로 정규화
- 최종 출력 형태: { "text": str }

📌 사용 시점:
- pipeline 상에서 "type": "input", "module": "fill_mask_input"

📌 지원 형태:
1. 문자열(str) 입력 (예: "The capital of France is [MASK].")
2. dict(text=...) 형태
3. 입력 없이 params["text"]로 제공되는 경우
"""

from typing import Any, Dict
from utils.text_input import extract_text_field


def run(input: Any = None, **params) -> Dict[str, str]:
    # 📌 run(): 마스킹 포함 텍스트를 text 필드로 정규화하여 반환

    # ✅ 공통 유틸을 사용하여 텍스트 추출
    text = extract_text_field(input, **params)

    # 📤 정규화된 결과 반환
    return { "text": text }