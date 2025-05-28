import importlib

# ------------------------------------------------------
# 📦 모듈 유형 → 실제 import 경로 기본 패키지 매핑
# - 모듈 타입(input/model/output 등)에 따라 import 경로 prefix 설정
# ------------------------------------------------------
TYPE_TO_PACKAGE = {
    "input": "adapters.input",
    "model": "models",
    "output": "adapters.output",
    "evaluator": "evaluators",
    "bridge": "adapters.bridge"
}

# ------------------------------------------------------
# 📌 커스텀 명령어 alias (모듈 명 → 실제 import 경로)
# - 가독성을 위해 추상화된 모듈 이름을 실제 경로로 매핑
# - 예: "text-model" → "models"
# ------------------------------------------------------
MODULE_ALIASES = {
    "text-model": "models",
    "vision-model": "models.vision",    
    "audio-model": "models.audio",
    "multimodal-model": "models.multimodal"
    # 🔧 확장 가능: 필요 시 여기에 추가
}

# ------------------------------------------------------
# 📌 동적 모듈 로딩 함수
# - 지정된 타입과 이름을 기반으로 importlib을 통해 모듈 동적 import
# - alias 등록 여부에 따라 처리 경로가 달라짐
# ------------------------------------------------------
def load_module(module_type: str, module_name: str):
    """
    ✅ 동적으로 모듈을 import하여 반환

    - TYPE_TO_PACKAGE + module_name 조합으로 기본 경로 구성
    - 또는 MODULE_ALIASES에 등록된 이름인 경우 실제 경로로 해석

    예:
    - ("model", "text-model") → models (text dispatcher)
    - ("model", "vision-model") → models.vision
    - ("bridge", "text.from_ner") → adapters.bridge.text.from_ner
    """

    # 🚨 예외처리: 지원하지 않는 모듈 유형
    if module_type not in TYPE_TO_PACKAGE:
        raise ValueError(f"❌ Unknown module type: {module_type}")

    # ✅ alias로 등록된 모델 이름인 경우 → alias 경로로 import
    if module_type == "model" and module_name in MODULE_ALIASES:
        resolved_path = MODULE_ALIASES[module_name]
        return importlib.import_module(resolved_path)

    # 🔄 일반 경로 조합: 기본 패키지 + 모듈 이름
    base_package = TYPE_TO_PACKAGE[module_type]
    full_path = f"{base_package}.{module_name}"

    # 📥 import 시도 + 예외 처리 래핑
    try:
        return importlib.import_module(full_path)
    except ImportError as e:
        raise ImportError(f"Module load failed: {full_path}") from e