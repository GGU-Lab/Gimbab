"""
📦 Output Adapter: json_output
──────────────────────────────────────────────
- 모델 실행 결과(리스트, 딕셔너리 등)를 보기 좋게 JSON-compatible 객체로 변환
- 주로 파이프라인의 마지막 노드로 사용됨
- 직렬화 후 출력: 프론트 전달, 로그 출력 등에 적합

📌 입력 예시:
[
  { "label": "POSITIVE", "score": 0.98 },
  { "label": "NEGATIVE", "score": 0.02 }
]

📌 출력 예시:
[
  {
    "label": "POSITIVE",
    "score": 0.98
  },
  {
    "label": "NEGATIVE",
    "score": 0.02
  }
]
"""

import traceback
from fastapi.encoders import jsonable_encoder
from utils.serialization import to_serializable

# ---------------------------------------------------
# 📌 JSON-compatible 변환 실행 함수
# ---------------------------------------------------
def run(input: any, **params):
    """
    📌 입력값을 JSON-compatible 객체로 변환하여 반환

    ✅ 인자:
    - input: dict 또는 list 형태의 실행 결과
    - **params: 향후 확장 가능 (미사용)

    ✅ 내부 처리 흐름:
    1. to_serializable: numpy, tensor 등 불가능 타입 정리
    2. jsonable_encoder: FastAPI가 응답으로 반환 가능하도록 변환
    """
    print("🚀 [json_output] run() 시작됨")
    print(f"📥 원본 input 타입: {type(input)}")

    try:
        # ✅ 내부 타입을 직렬화 가능하게 변환
        safe_input = to_serializable(input)
        print("✅ 최종 직렬화 대상 데이터:")
        print(safe_input)

        # ✅ FastAPI 응답에서 안전하게 처리할 수 있도록 jsonable_encoder 적용
        encoded = jsonable_encoder(safe_input)
        print("✅ FastAPI jsonable_encoder 처리 완료")

        return encoded

    except Exception as e:
        print("❌ JSON 출력 직전 예외 발생:")
        traceback.print_exc()
        raise 