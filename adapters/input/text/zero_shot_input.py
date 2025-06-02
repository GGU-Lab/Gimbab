"""
📦 Input Adapter: zero_shot_input
──────────────────────────────────────────────
- 텍스트와 라벨 리스트를 받아 zero-shot 분류 입력 구조로 정규화
- 최종 출력 형태: { "text": str, "labels": List[str] }

📌 사용 시점:
- pipeline 상에서 "type": "input", "module": "zero_shot_input"

📌 지원 형태:
1. input이 dict인 경우: text + labels 직접 제공
2. input이 str이고 labels는 params로 제공되는 경우
3. text가 params["text"]로만 주어지고, input은 없는 경우
"""

from typing import Any, Dict, List
from utils.text_input import extract_text_field


def run(input: Any = None, **params) -> Dict[str, Any]:
    # 📌 run(): 입력 + 파라미터에서 text, labels 정보를 정규화하여 반환

    # ✅ text 추출 (공통 유틸 사용)
    text = extract_text_field(input, **params)

    # ✅ labels 추출
    if isinstance(input, dict) and "labels" in input:
        labels = input["labels"]
    else:
        labels = params.get("labels", [])

    # ✅ labels 정규화: 문자열이면 쉼표 기준 분할, 그 외는 리스트로 변환
    if isinstance(labels, str):
        labels = [label.strip() for label in labels.split(",")]
    elif not isinstance(labels, list):
        labels = [str(labels)]

    # 📤 정규화된 결과 반환
    return { "text": text, "labels": labels }