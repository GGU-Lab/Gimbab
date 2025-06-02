"""
📦 Text2Text Generation 실행기
──────────────────────────────────────────────
- text2text-generation 태스크 실행
- 입력 텍스트에 대해 다양한 목적의 텍스트 생성 (T5, FLAN-T5, BART 등)
- model_name 지정 가능, 캐싱 처리 포함
"""

from transformers import pipeline

_cached_models = {}

def run(input, model_name=None, reload=False, **kwargs):
    # 📌 run(): text2text-generation 태스크용 pipeline 실행 (캐시 포함)
    key = f"text2text-generation:{model_name or 'default'}"

    # ✅ 모델 캐싱 또는 강제 재로딩 처리
    if reload or key not in _cached_models:
        _cached_models[key] = pipeline("text2text-generation", model=model_name)

    pipe = _cached_models[key]

    # 📤 생성 실행 (예: 번역, 요약, QA 등 프롬프트 기반 처리 가능)
    return pipe(input["text"], **kwargs)