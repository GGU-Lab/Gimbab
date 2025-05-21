"""
📦 Evaluator: resource_logger
──────────────────────────────────────────────
- 실행 대상 모듈의 입력/출력에 대해 리소스 측정 로그 출력
- 메모리 사용량 (byte) 및 토큰 수(단어 수 기반 추정)를 로깅
- 디버깅 및 성능 최적화 분석에 유용

📌 출력 예시:
📦 resource_logger: hf_pipeline_runner
  - input size:  324 bytes, tokens: 10
  - output size: 728 bytes, tokens: 40
"""

import sys

# ---------------------------------------------------
# 📌 객체 크기 측정 유틸 함수
# - sys.getsizeof 기반 단순 메모리 추정
# ---------------------------------------------------
def get_size(obj):
    try:
        return sys.getsizeof(obj)
    except Exception:
        return 0

# ---------------------------------------------------
# 📌 토큰 수 추정 유틸 함수
# - 공백 기준 split 사용 (임시 기준, 추후 tokenizer 대체 가능)
# ---------------------------------------------------
def count_tokens(text):
    if not isinstance(text, str):
        return 0
    return len(text.split())

# ---------------------------------------------------
# 📌 evaluator 실행 함수
# - 입력 크기 및 출력 크기를 측정하고 로그로 출력
# - 실행 대상은 module.run(input, **params)
# ---------------------------------------------------
def run(input: any, **params):
    module = params.pop("module", None)

    # 🚨 필수 조건: module 객체는 반드시 run()을 가져야 함
    if module is None or not hasattr(module, "run"):
        raise ValueError("resource_logger requires a valid 'module' with a 'run' method.")

    # ✅ 입력 리소스 측정
    input_size = get_size(input)
    input_tokens = count_tokens(str(input))

    # 🔁 실제 실행
    result = module.run(input, **params)

    # ✅ 출력 리소스 측정
    output_size = get_size(result)
    output_tokens = count_tokens(str(result))

    # 🪵 리소스 로그 출력
    print(f"📦 resource_logger: {getattr(module, '__name__', module.__class__.__name__)}")
    print(f"  - input size:  {input_size} bytes, tokens: {input_tokens}")
    print(f"  - output size: {output_size} bytes, tokens: {output_tokens}")

    # ✅ 실행 결과 그대로 반환
    return result