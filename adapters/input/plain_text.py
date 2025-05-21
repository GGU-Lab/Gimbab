"""
📦 Input Adapter: plain_text
──────────────────────────────────────────────
- 다양한 방식의 입력(text)을 받아 일관된 구조로 변환
- 최종 출력 형태는 항상: { "text": ... }

📌 사용 시점:
- pipeline 상에서 "type": "input", "module": "plain_text" 형태로 사용됨

📌 지원 형태:
1. 문자열(str) 입력: 그대로 text로 감싸기
2. 이미 정규화된 dict 입력: 그대로 통과
3. 입력이 없고 params로만 들어올 경우: 파라미터 기반 처리
"""

def run(input: any = None, **params):
    # ✅ 1. 문자열 입력인 경우 → text 필드로 감싸기
    if isinstance(input, str):
        return { "text": input }

    # ✅ 2. 이미 정규화된 dict가 들어온 경우 → 그대로 사용
    if isinstance(input, dict) and "text" in input:
        return input

    # ✅ 3. 명시적 입력이 없고, text가 파라미터로 들어온 경우
    text = params.get("text", "")
    return { "text": text }