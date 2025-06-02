"""
📦 Text Generation 실행기
──────────────────────────────────────────────
- text-generation 태스크 실행 (예: GPT2, GPT-J 등)
- 자유 생성(generative) 모델을 기반으로 후속 텍스트 생성
- model_name 지정 가능, 캐싱 처리 포함
"""

from transformers import pipeline

_cached_models = {}

def run(input, model_name=None, reload=False, **kwargs):
    # 📌 run(): 텍스트 생성 태스크용 pipeline 실행 (캐시 포함)
    key = f"text-generation:{model_name or 'default'}"

    # ✅ 모델 캐싱 또는 강제 재로딩 처리
    if reload or key not in _cached_models:
        _cached_models[key] = pipeline("text-generation", model=model_name)

    pipe = _cached_models[key]

    # 📤 생성 실행 (max_new_tokens 등은 kwargs로 제어)
    return pipe(input["text"], **kwargs)
