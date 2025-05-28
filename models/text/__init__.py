"""
📦 Text Task Dispatcher
──────────────────────────────────────────────
- 입력된 task 이름에 따라 알맞은 실행기로 분기 처리
- sentiment / ner / zero-shot / translation 등 텍스트 기반 태스크를 처리함
"""

from .sentiment import run as run_sentiment
from .ner import run as run_ner
from .zero_shot import run as run_zero_shot
from .translation import run as run_translation

def run(input, task, model_name=None, reload=False, **kwargs):
    # 📌 run(): 태스크명을 기반으로 각 전용 실행기(run_*)로 분기 수행

    # ✅ 감정 분석 태스크
    if task == "sentiment-analysis":
        return run_sentiment(input, model_name, reload)

    # ✅ 개체명 인식(NER) 태스크
    elif task == "ner":
        return run_ner(input, model_name, reload)

    # ✅ 제로샷 분류 태스크 (라벨 후보 필요)
    elif task == "zero-shot-classification":
        return run_zero_shot(input, model_name, reload, **kwargs)

    # ✅ 번역/요약/text2text 생성 등 (같은 실행기 사용)
    elif task in ["translation", "summarization", "text2text-generation"]:
        return run_translation(input, task, model_name, reload)

    # ❌ 미지원 태스크 입력 시 예외 처리
    else:
        raise ValueError(f"❌ Unsupported text task: {task}")