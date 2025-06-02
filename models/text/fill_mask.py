"""
📦 Fill-Mask 실행기
──────────────────────────────────────────────
- fill-mask 태스크 실행 (예: BERT [MASK] 채우기)
- 입력 텍스트에 마스킹된 위치를 기반으로 가능한 토큰을 예측
- model_name 지정 가능, 캐싱 처리 포함
"""

from transformers import pipeline

_cached_models = {}

def run(input, model_name=None, reload=False):
    # 📌 run(): fill-mask 태스크용 pipeline 실행 (캐시 포함)
    key = f"fill-mask:{model_name or 'default'}"

    # ✅ 모델 캐싱 또는 강제 재로딩 처리
    if reload or key not in _cached_models:
        _cached_models[key] = pipeline("fill-mask", model=model_name)

    pipe = _cached_models[key]

    # 📤 마스크 예측 실행
    return pipe(input["text"])