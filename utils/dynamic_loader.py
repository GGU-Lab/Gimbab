import importlib

# ------------------------------------------------------
# 📌 모듈 유형 → 실제 패키지 경로 매핑
# - 실행 시 module_type에 따라 import할 경로를 결정함
# - 각 유형별 폴더 이름과 연결
# ------------------------------------------------------
TYPE_TO_PACKAGE = {
    "input": "adapters.input",         # 입력 처리 모듈
    "model": "models",                 # 모델 실행 모듈
    "output": "adapters.output",       # 출력 포맷 모듈
    "evaluator": "evaluators",         # 평가기 모듈
}

# ------------------------------------------------------
# 📌 동적 모듈 로더
# - 주어진 모듈 유형(type)과 이름(name)을 기반으로
#   실제 실행 가능한 모듈을 import하여 반환
# ------------------------------------------------------
def load_module(module_type: str, module_name: str):
    """
    📌 문자열 기반 모듈 로더

    ✅ 인자:
    - module_type: "input", "model", "output", "evaluator" 중 하나
    - module_name: 실제 파일 이름 (예: plain_text, json_output)

    🔄 예:
    - ("model", "hf_pipeline_runner") → models.hf_pipeline_runner 모듈 import
    - ("input", "plain_text") → adapters.input.plain_text import

    ❗ 예외 처리:
    - 지원하지 않는 타입 → ValueError
    - 해당 모듈이 없을 경우 → ImportError
    """

    # 🚨 정의되지 않은 타입인 경우 예외 처리
    if module_type not in TYPE_TO_PACKAGE:
        raise ValueError(f"Unknown module type: {module_type}")

    # ✅ 모듈 경로 조합: 예) models.hf_pipeline_runner
    package_path = TYPE_TO_PACKAGE[module_type]
    full_path = f"{package_path}.{module_name}"

    try:
        # 🔁 동적으로 모듈 임포트
        module = importlib.import_module(full_path)
        return module

    except ImportError as e:
        # 🚨 모듈이 존재하지 않을 경우 예외 발생
        raise ImportError(f"Module load failed: {full_path}") from e