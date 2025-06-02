"""
📦 Input Adapter: qa_input
──────────────────────────────────────────────
- 질의응답(question answering) 태스크를 위한 입력 구조 정규화
- 최종 출력 형태: { "question": str, "context": str }

📌 사용 시점:
- pipeline 상에서 "type": "input", "module": "qa_input"

📌 지원 형태:
1. input이 dict인 경우: { question: ..., context: ... } 형태 직접 제공
2. params에서 각각 question/context가 주어지는 경우
"""

from typing import Any, Dict


def run(input: Any = None, **params) -> Dict[str, str]:
    print(f"[qa_input] input={input}")
    print(f"[qa_input] params={params}")

    # ✅ fallback 처리 개선: input이 dict이지만 비어 있으면 params 우선
    if isinstance(input, dict) and input:
        question = input.get("question", "")
        context = input.get("context", "")
    else:
        question = params.get("question", "")
        context = params.get("context", "")

    # 강제 문자열 변환
    return {
        "question": str(question),
        "context": str(context)
    }
