"""
📦 Input Adapter: plain_text
──────────────────────────────────────────────
- 다양한 방식의 입력(text)을 받아 일관된 구조로 변환
- 최종 출력 형태는 항상: { "text": ... } (dict)

📌 사용 시점:
- pipeline 상에서 "type": "input", "module": "plain_text" 형태로 사용됨

📌 지원 형태:
1. 문자열(str) 입력: 그대로 text로 감싸기
2. dict(text=...) 형태: 그대로 통과
3. 입력이 없고 params로만 들어올 경우: 파라미터 기반 처리
"""

from utils.text_input import extract_text_field


def run(input: any = None, **params) -> dict:
    # 📌 run(): 다양한 입력을 text 필드로 정규화하여 반환하는 어댑터

    # ✅ 공통 유틸을 사용하여 텍스트 추출
    text = extract_text_field(input, **params)

    # 📤 정규화된 결과 반환
    return { "text": text }