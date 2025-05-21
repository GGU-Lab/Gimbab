"""
📦 Evaluator 실행 유틸리티: evaluator_runner.py
──────────────────────────────────────────────
- 각 노드의 실행 모듈에 evaluator를 중첩 래핑하는 기능 제공
- evaluator는 클로저 방식으로 run() 메서드를 감싸는 구조
- 추후 evaluator 실행 결과 로깅, 저장, 후처리 확장 가능성 대비
"""

from typing import List
from utils.dynamic_loader import load_module

# ------------------------------------------------------
# 📌 Evaluator 래핑 함수
# - 실행 모듈을 evaluator로 감싸서 실행 중 평가 수행
# - 여러 evaluator를 중첩 적용 가능 (클로저 기반)
# ------------------------------------------------------
def apply_evaluators(module, evaluator_names: List[str]):
    """
    evaluator 목록에 따라 실행 모듈을 중첩 래핑합니다.

    ✅ 동작 방식:
    - evaluator.run(input=..., module=prev_module, **params) 형식으로 호출됨
    - 기존 모듈을 감싸는 형태로 순차적으로 evaluator를 적용합니다.

    ✅ 입력:
    - module: run(input=...) 메서드를 가진 실행 객체
    - evaluator_names: 문자열 evaluator 모듈 이름 목록

    ✅ 출력:
    - evaluator가 중첩 적용된 모듈 (run 메서드만 존재)
    """
    for evaluator_name in evaluator_names:
        evaluator_module = load_module("evaluator", evaluator_name)

        def make_wrapped(prev_module, evaluator_module):
            def run(input, **params):
                return evaluator_module.run(input=input, module=prev_module, **params)
            return type("WrappedModule", (), {"run": staticmethod(run)})()

        module = make_wrapped(module, evaluator_module)

    return module