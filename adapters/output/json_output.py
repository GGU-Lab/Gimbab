"""
📦 Output Adapter: json_output
──────────────────────────────────────────────
- 모델 실행 결과(리스트, 딕셔너리 등)를 보기 좋게 JSON 문자열로 변환
- 주로 파이프라인의 마지막 노드로 사용됨
- 직렬화 후 출력: 프론트 전달, 로그 출력 등에 적합

📌 입력 예시:
[
  { "label": "POSITIVE", "score": 0.98 },
  { "label": "NEGATIVE", "score": 0.02 }
]

📌 출력 예시:
"[
  {
    \"label\": \"POSITIVE\",
    \"score\": 0.98
  },
  {
    \"label\": \"NEGATIVE\",
    \"score\": 0.02
  }
]"
"""

import json

# ---------------------------------------------------
# 📌 JSON 직렬화 실행 함수
# - input: dict, list 등 JSON 직렬화 가능한 구조체
# - indent, ensure_ascii 등은 파라미터 커스터마이징 가능
# ---------------------------------------------------
def run(input: any, **params):
    """
    📌 입력값을 JSON 문자열로 직렬화하여 반환

    ✅ 인자:
    - input: dict 또는 list 형태의 실행 결과
    - **params: json.dumps에 넘길 추가 설정 (예: indent, ensure_ascii 등)

    ✅ 기본 설정:
    - indent=2: 보기 좋게 들여쓰기
    - ensure_ascii=False: 한글 등 유니코드 출력 유지
    """
    return json.dumps(input, ensure_ascii=False, indent=2)