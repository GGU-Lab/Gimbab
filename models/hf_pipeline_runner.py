"""
📦 Model Adapter: hf_pipeline_runner
──────────────────────────────────────────────
- HuggingFace의 transformers.pipeline을 기반으로 동작
- 다양한 태스크(sentiment-analysis, ner, translation 등)에 대응 가능
- 모델 이름과 태스크명을 기반으로 동적으로 pipeline 생성
- 실행 속도를 위해 캐싱 구조(_cached_models) 사용

📌 입력 예시:
{
    "text": "오늘 기분 좋아요"
}

📌 파라미터 예시:
task="sentiment-analysis", model_name="beomi/kcbert-base"
"""

from transformers import pipeline

# ✅ 모델 인스턴스 캐싱 (task:모델명 기준)
_cached_models = {}

# ---------------------------------------------------
# 📌 모델 실행 함수
# - 입력 데이터를 받아 지정한 task로 추론 수행
# - 동일 task/model 조합은 캐시 재사용
# ---------------------------------------------------
def run(
    input: dict | str | list,
    task: str = "sentiment-analysis",
    model_name: str = None,
    reload: bool = False,
    **kwargs
):
    """
    HuggingFace pipeline 실행기

    ✅ 인자:
    - input: dict, str, list 모두 지원
        - {"text": "..."} 형태 (기본 권장)
        - 단일 문자열 또는 리스트 형태도 가능
    - task: 감성 분석, 번역, 요약 등 pipeline 태스크
    - model_name: 사용할 모델 이름 (예: beomi/kcbert-base)
    - reload: True일 경우 기존 캐시 무시하고 재로딩

    📌 주의사항:
    - model1 → model2 연결 시, input이 list/dict 형태일 수 있음
    - 가능한한 유연하게 처리되도록 설계
    """

    # ✅ 모델 캐싱 키 생성: 예) "sentiment-analysis:beomi/kcbert-base"
    key = f"{task}:{model_name or 'default'}"

    # 🔄 캐시가 없거나 reload 요청 시 새로 로딩
    if reload or key not in _cached_models:
        _cached_models[key] = pipeline(task, model=model_name)

    pipe = _cached_models[key]

    # ---------------------------------------------------
    # ✅ 태스크 유형별 입력 처리
    # ---------------------------------------------------

    if task in ["sentiment-analysis", "ner", "zero-shot-classification"]:
        # ✅ 이 태스크들은 문자열(text) 또는 단순 dict 입력을 기대

        if isinstance(input, str):
            return pipe(input)

        elif isinstance(input, dict):
            return pipe(input.get("text", str(input)))

        elif isinstance(input, list):
            # ✅ list of text or dict: 각각 개별 처리
            return [pipe(i.get("text", str(i)) if isinstance(i, dict) else str(i)) for i in input]

        else:
            raise ValueError(f"❌ 지원되지 않는 입력 형식: {type(input)}")

    elif task in ["translation", "summarization", "text2text-generation"]:
        # ✅ 이 태스크들은 dict, str, list 모두 가능
        return pipe(input)

    else:
        # 🚨 정의되지 않은 태스크: fallback 처리
        return pipe(str(input))