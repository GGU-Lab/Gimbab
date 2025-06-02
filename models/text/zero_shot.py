"""
📦 Zero-shot 실행기
──────────────────────────────────────────────
- zero-shot-classification 태스크 실행
- candidate_labels 필수, 문자열 또는 리스트 형태 모두 지원
- input["labels"]에서 자동 추출도 지원 (InputAdapter에서 올 경우 대응)
"""

from transformers import pipeline

def run(input, model_name=None, reload=False, **kwargs):
    # 📌 run(): 주어진 후보 라벨(candidate_labels 또는 input["labels"]) 기반 제로샷 분류 수행
    pipe = pipeline("zero-shot-classification", model=model_name)

    # ✅ 입력 텍스트 추출
    text = input["text"]

    # ✅ 라벨 목록 추출: params 우선, 없으면 input 내부 "labels" 사용
    candidate_labels = kwargs.get("candidate_labels") or input.get("labels", [])

    # ✅ 문자열 하나로 전달된 경우 쉼표로 분리
    if isinstance(candidate_labels, str):
        candidate_labels = [x.strip() for x in candidate_labels.split(",")]

    # ❌ 라벨이 비어있을 경우 예외 발생
    if not candidate_labels:
        raise ValueError("❌ candidate_labels required for zero-shot-classification.")

    # 📤 제로샷 분류 실행 결과 반환
    return pipe(text, candidate_labels=candidate_labels)