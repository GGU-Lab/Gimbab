from transformers import pipeline

# ✅ 모델 캐시 저장소
# - 동일 task/model_name 조합은 중복 로딩 없이 재사용
_cached_models = {}

# ----------------------------------------------------
# 📌 모델 실행기 (Model Adapter)
# - HuggingFace pipeline 기반으로 다양한 task 처리
# - 입력 형식에 따라 분기 처리
# - zero-shot 등 특수 태스크는 별도 로직 적용
# ----------------------------------------------------
def run(
    input: dict | str | list,
    task: str = "sentiment-analysis",
    model_name: str = None,
    reload: bool = False,
    **kwargs
):
    # ✅ 캐시 키 구성: task + model_name
    key = f"{task}:{model_name or 'default'}"

    # ✅ 모델 캐싱: zero-shot은 candidate_labels가 실행 시점마다 다를 수 있어 제외
    if reload or key not in _cached_models:
        if task == "zero-shot-classification":
            # ⚠️ zero-shot은 매번 candidate_labels가 다를 수 있으므로 캐시 생략
            pipe = pipeline(task, model=model_name)
        else:
            # 일반 태스크는 캐시 등록
            _cached_models[key] = pipeline(task, model=model_name)
            pipe = _cached_models[key]
    else:
        pipe = _cached_models[key]

    # ----------------------------------------------------
    # ✅ 태스크별 입력 처리 분기
    # ----------------------------------------------------

    # 1. 감성 분석, NER 등: text 입력이 필요
    if task in ["sentiment-analysis", "ner"]:
        if isinstance(input, str):
            return pipe(input)
        elif isinstance(input, dict):
            return pipe(input.get("text", str(input)))  # {"text": "..."} 구조 기대
        elif isinstance(input, list):
            return [
                pipe(i.get("text", str(i)) if isinstance(i, dict) else str(i))
                for i in input
            ]
        else:
            raise ValueError(f"❌ 지원되지 않는 입력 형식: {type(input)}")

    # 2. zero-shot classification: 입력 문장 + candidate_labels 필요
    elif task == "zero-shot-classification":
        # ✅ 입력 텍스트 추출
        if isinstance(input, dict):
            text = input.get("text", "")
        else:
            text = str(input)

        # ✅ candidate_labels 추출 및 문자열 → 리스트 처리
        candidate_labels = kwargs.get("candidate_labels", [])
        if isinstance(candidate_labels, str):
            candidate_labels = [x.strip() for x in candidate_labels.split(",")]

        # 🚨 필수 파라미터 누락 시 예외 발생
        if not candidate_labels:
            raise ValueError("❌ candidate_labels가 zero-shot-classification에 필요합니다.")

        return pipe(text, candidate_labels=candidate_labels)

    # 3. 번역, 요약, 텍스트 생성 계열: pipe(input)만으로 동작
    elif task in ["translation", "summarization", "text2text-generation"]:
        return pipe(input)

    # 4. 기타 태스크 (fallback): string 처리
    else:
        return pipe(str(input))