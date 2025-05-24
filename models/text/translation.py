"""
📦 Translation/Text2Text 실행기
──────────────────────────────────────────────
- 번역 / 요약 / text2text-generation 태스크 실행
- task에 따라 동적 pipeline 생성
"""

from transformers import pipeline

_cached_models = {}

def run(input, task="translation", model_name=None, reload=False):
    # 📌 run(): task 종류에 따른 텍스트 생성 pipeline 실행
    key = f"{task}:{model_name or 'default'}"

    # ✅ 모델 캐싱 또는 강제 재로딩 처리
    if reload or key not in _cached_models:
        _cached_models[key] = pipeline(task, model=model_name)

    pipe = _cached_models[key]

    # 📤 단일 문장 또는 복수 문장에 대해 실행
    return pipe(input["text"])