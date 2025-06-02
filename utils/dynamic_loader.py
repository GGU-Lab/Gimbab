import importlib

# ------------------------------------------------------
# 📦 모듈 유형 → 실제 import 경로 기본 패키지 매핑
# ------------------------------------------------------
TYPE_TO_PACKAGE = {
    "input": "adapters.input",
    "model": "models",
    "output": "adapters.output",
    "evaluator": "evaluators",
    "bridge": "adapters.bridge"
}

# ------------------------------------------------------
# 📌 모델 alias 정의 (model 타입 전용)
# ------------------------------------------------------
MODULE_ALIASES = {
    "text-model": "models",
    "vision-model": "models.vision",
    "audio-model": "models.audio",
    "multimodal-model": "models.multimodal"
    # 🔧 확장 가능
}

# ------------------------------------------------------
# 📌 모듈 로딩 함수 (text.모델명 구조 기준)
# ------------------------------------------------------
def load_module(module_type: str, module_name: str):
    """
    ✅ 모듈 타입과 이름 기반으로 importlib을 통해 동적 import

    사용 예:
    - ("input", "text.zero_shot_input")    → adapters.input.text.zero_shot_input
    - ("bridge", "text.from_translation")  → adapters.bridge.text.from_translation
    - ("model", "text-model")              → models  (alias 처리)
    - ("model", "my_model")                → models.my_model
    """

    # 🚫 지원되지 않는 타입 예외 처리
    if module_type not in TYPE_TO_PACKAGE:
        raise ValueError(f"❌ Unknown module type: {module_type}")

    # 🎯 alias 적용 (model 전용)
    if module_type == "model" and module_name in MODULE_ALIASES:
        resolved_path = MODULE_ALIASES[module_name]
        return importlib.import_module(resolved_path)

    # 📦 경로 조합
    base_package = TYPE_TO_PACKAGE[module_type]
    full_path = f"{base_package}.{module_name}"

    try:
        return importlib.import_module(full_path)
    except ImportError as e:
        raise ImportError(f"Module load failed: {full_path}") from e