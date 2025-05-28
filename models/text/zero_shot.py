"""
📦 Zero-shot 실행기
──────────────────────────────────────────────
- zero-shot-classification 태스크 실행
- candidate_labels 필수, 문자열 또는 리스트 형태 모두 지원
"""

from transformers import pipeline

def run(input, model_name=None, reload=False, **kwargs):
    # 📌 run(): 주어진 후보 라벨(candidate_labels) 기반 제로샷 분류 수행
    pipe = pipeline("zero-shot-classification", model=model_name)

    text = input["text"]
    candidate_labels = kwargs.get("candidate_labels", [])

    # ✅ 문자열 하나로 전달된 경우 쉼표 분리 처리
    if isinstance(candidate_labels, str):
        candidate_labels = [x.strip() for x in candidate_labels.split(",")]

    # ❌ 라벨이 비어있을 경우 예외 발생
    if not candidate_labels:
        raise ValueError("❌ candidate_labels required for zero-shot-classification.")

    # 📤 분류 실행 결과 반환
    return pipe(text, candidate_labels=candidate_labels)