"""
📦 Utils: text_input
──────────────────────────────────────────────
텍스트 기반 InputAdapter들이 공통적으로 사용하는 입력 정규화 함수 제공

🎯 목적:
- 다양한 입력 형태(input, params)로부터 "text" 필드를 안정적으로 추출
- 모든 입력을 문자열(str)로 강제 변환하여 반환
"""

from typing import Any


def extract_text_field(input: Any = None, **params) -> str:
    """
    다양한 입력(input + params)에서 'text' 필드를 추출하여 문자열로 반환

    📌 지원 형태:
    1. input이 str: 그대로 반환
    2. input이 dict + "text" 키 포함: 해당 값 반환
    3. 명시적 input이 없고 params["text"]만 있을 경우: 해당 값 반환
    4. text가 str이 아닐 경우: str()로 강제 변환

    ⚠️ "text"가 전혀 없을 경우 빈 문자열 반환 (필요 시 raise 가능)
    """
    # ✅ case 1: input이 str이면 바로 반환
    if isinstance(input, str):
        return input

    # ✅ case 2: dict 형태의 input에서 "text" 필드 존재
    if isinstance(input, dict) and "text" in input:
        return input["text"]

    # ✅ case 3: text가 params에 있는 경우
    text = params.get("text", "")

    # ✅ case 4: str 강제 변환
    return str(text)