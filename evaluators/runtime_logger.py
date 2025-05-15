"""
📦 Evaluator: runtime_logger
──────────────────────────────────────────────
- 대상 모듈(module.run)을 실행하면서 실행 시간을 측정함
- 성능 모니터링 또는 디버깅 목적에 유용
- 입력/출력 데이터는 수정 없이 그대로 통과시킴

📌 사용 예:
- evaluator로 등록 시, 해당 노드의 실행 시간을 로그로 출력
- 예: "runtime_logger: hf_pipeline_runner.run() took 0.2312 seconds"
"""

import time

# ---------------------------------------------------
# 📌 evaluator 실행 함수
# - 파이프라인 노드 실행 전후로 시간 측정
# - 실제 실행은 전달받은 module.run에 위임
# ---------------------------------------------------
def run(input: any, **params):
    # ✅ 평가 대상 모듈 (중첩 evaluator가 감싼 모듈 포함)
    module = params.pop("module", None)

    # 🚨 유효성 검사: 반드시 module.run이 존재해야 함
    if module is None or not hasattr(module, "run"):
        raise ValueError("runtime_logger requires a valid 'module' with a 'run' method.")

    # ✅ 실행 시간 측정 시작
    start_time = time.time()

    # 🔁 원래 모듈 실행
    result = module.run(input, **params)

    # ✅ 시간 측정 종료
    elapsed = time.time() - start_time

    # 🪵 로그 출력 (모듈 이름 또는 미지정 시 문자열 fallback)
    module_name = getattr(module, "__name__", str(module))
    print(f"⏱️ runtime_logger: {module_name}.run() took {elapsed:.4f} seconds")

    # ✅ 결과 그대로 반환
    return result