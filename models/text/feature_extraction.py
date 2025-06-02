"""
📦 Feature Extraction 실행기
──────────────────────────────────────────────
- feature-extraction 태스크 실행
- 텍스트를 고차원 임베딩 벡터로 변환
- model_name 지정 가능, 캐싱 처리 포함
"""

from transformers import pipeline

_cached_models = {}

def run(input, model_name=None, reload=False):
    # 📌 run(): feature-extraction 태스크용 pipeline 실행 (캐시 포함)
    key = f"feature-extraction:{model_name or 'default'}"

    # ✅ 모델 캐싱 또는 강제 재로딩 처리
    if reload or key not in _cached_models:
        _cached_models[key] = pipeline("feature-extraction", model=model_name)

    pipe = _cached_models[key]

    # 📤 텍스트 임베딩 실행
    return pipe(input["text"])