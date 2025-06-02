"""
📦 Question Answering 실행기
──────────────────────────────────────────────
- question-answering 태스크 실행
- 주어진 질문과 문맥(context)을 기반으로 답변 추출
- model_name 지정 가능, 캐싱 및 로깅 처리 포함
"""

from transformers import pipeline

_cached_models = {}

def run(input, model_name=None, reload=False):
    # 📌 run(): question-answering 태스크용 pipeline 실행 (캐시 및 검증 포함)
    key = f"question-answering:{model_name or 'default'}"

    # ✅ 모델 캐싱 또는 강제 재로딩 처리
    if reload or key not in _cached_models:
        print(f"[LOAD MODEL] task=question-answering | model={model_name}")
        _cached_models[key] = pipeline("question-answering", model=model_name)

    pipe = _cached_models[key]

    # ✅ 입력 로그 출력 (디버깅 용도)
    print(f"[RUN] Received input: {input}")
    print(f"[RUN] model_name: {model_name}")

    # 🚫 입력 타입 확인: dict가 아닐 경우 예외 처리
    if not isinstance(input, dict):
        print(f"[ERROR] Input is not a dict! Type: {type(input)}")
        raise TypeError(f"❌ Invalid input type for QA task: {type(input)}. Expected dict.")

    # 🧾 질문 및 문맥 추출
    question = input.get("question")
    context = input.get("context")

    # 🚫 필수 항목 누락 검사
    if not question or not context:
        print(f"[ERROR] Missing question/context | question={question} | context={context}")
        raise ValueError("❌ question-answering requires both 'question' and 'context'.")

    # ✅ 실행 로그: 실제 실행되는 질의 정보 표시
    print(f"[EXECUTE] QA: {question} / {len(context)} chars context")

    # 📤 질의응답 파이프라인 실행
    return pipe({ "question": question, "context": context })