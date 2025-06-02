"""
📦 Text Task Dispatcher
──────────────────────────────────────────────
- 입력된 task 이름에 따라 알맞은 실행기로 분기 처리
- sentiment / ner / zero-shot / translation / summarization / QA 등
  텍스트 기반 태스크 전반을 지원함
"""

from .sentiment import run as run_sentiment
from .ner import run as run_ner
from .zero_shot import run as run_zero_shot
from .translation import run as run_translation
from .summarization import run as run_summarization
from .question_answering import run as run_qa
from .text_generation import run as run_text_generation
from .fill_mask import run as run_fill_mask
from .feature_extraction import run as run_feature_extraction
from .text2text import run as run_text2text


def run(input, task, model_name=None, reload=False, **kwargs):
    # 📌 run(): 태스크명을 기반으로 각 전용 실행기로 분기 처리

    if task == "sentiment-analysis":
        return run_sentiment(input, model_name, reload)

    elif task == "ner":
        return run_ner(input, model_name, reload)

    elif task == "zero-shot-classification":
        return run_zero_shot(input, model_name, reload, **kwargs)

    elif task == "translation":
        return run_translation(input, task="translation", model_name=model_name, reload=reload)

    elif task == "summarization":
        return run_summarization(input, model_name, reload)

    elif task == "question-answering":
        return run_qa(input, model_name, reload)

    elif task == "text-generation":
        return run_text_generation(input, model_name, reload, **kwargs)

    elif task == "fill-mask":
        return run_fill_mask(input, model_name, reload)

    elif task == "feature-extraction":
        return run_feature_extraction(input, model_name, reload)

    elif task == "text2text-generation":
        return run_text2text(input, model_name, reload, **kwargs)

    else:
        raise ValueError(f"❌ Unsupported text task: {task}")