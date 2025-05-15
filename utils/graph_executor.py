from typing import List, Dict, Any
from collections import defaultdict, deque
from utils.dynamic_loader import load_module

# ------------------------------------------------------
# 📌 위상 정렬 함수: 실행 순서를 결정 (선행 → 후속)
# - DAG(방향성 비순환 그래프)에서 노드 순서를 정렬
# - 순환(cycle)이 감지되면 오류 발생
# ------------------------------------------------------
def topological_sort(nodes: List[Dict], edges: List[Dict]) -> List[str]:
    graph = defaultdict(list)      # 각 노드의 인접 노드 목록
    indegree = defaultdict(int)    # 각 노드의 진입 차수

    # ✅ 간선 정보로부터 그래프 생성
    for edge in edges:
        graph[edge["from"]].append(edge["to"])
        indegree[edge["to"]] += 1

    # ✅ 진입 차수가 0인 노드를 큐에 삽입
    queue = deque([node["id"] for node in nodes if indegree[node["id"]] == 0])
    result = []

    # 🔁 위상 정렬 수행 (Kahn’s Algorithm)
    while queue:
        current = queue.popleft()
        result.append(current)
        for neighbor in graph[current]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    # 🚨 사이클이 존재하는 경우 예외 처리
    if len(result) != len(nodes):
        raise ValueError("Cycle detected in DAG.")

    return result

# ------------------------------------------------------
# 📌 Evaluator 래핑 함수
# - 실행 모듈에 대해 평가기(evaluator)를 중첩 적용
# - evaluator는 module.run(input=input, module=prev_module, **params) 형식으로 호출됨
# ------------------------------------------------------
def apply_evaluators(module, evaluator_names: List[str]):
    """
    여러 evaluator를 중첩 적용하는 클로저 기반 evaluator 래퍼
    - 입력: 원본 모듈, evaluator 이름 목록
    - 출력: evaluator가 래핑된 모듈(run 메서드를 가진 객체)
    """

    for evaluator_name in evaluator_names:
        evaluator_module = load_module("evaluator", evaluator_name)

        # ✅ 클로저를 이용해 evaluator를 래핑한 새로운 모듈 생성
        def make_wrapped(prev_module, evaluator_module):
            def run(input, **params):
                return evaluator_module.run(input=input, module=prev_module, **params)
            
            # 익명 클래스: run 메서드만 포함
            return type("WrappedModule", (), {"run": staticmethod(run)})()

        module = make_wrapped(module, evaluator_module)

    return module

# ------------------------------------------------------
# 📌 전체 그래프 실행 함수
# - 위상 정렬을 기반으로 각 노드를 순서대로 실행
# - evaluator가 존재하면 실행 모듈을 감싼 후 run
# ------------------------------------------------------
def execute_graph(nodes: List[Dict[str, Any]], edges: List[Dict[str, str]]) -> Dict[str, Any]:
    node_map = {node["id"]: node for node in nodes}          # id → 노드 정의
    edge_map = defaultdict(list)                             # 현재 노드 ← 이전 노드 목록

    # 🔁 edges로부터 입력 연결 관계 구성
    for edge in edges:
        edge_map[edge["to"]].append(edge["from"])

    # ✅ 위상 정렬: 실행 순서 결정
    sorted_node_ids = topological_sort(nodes, edges)

    results = {}  # 각 노드의 실행 결과 저장소

    # 🔁 정렬된 순서대로 노드 실행
    for node_id in sorted_node_ids:
        node = node_map[node_id]
        input_data = {}

        # 🔄 연결된 이전 노드들의 출력 결과 수집
        for prev_id in edge_map[node_id]:
            input_data[prev_id] = results[prev_id]

        module_type = node["type"]             # 예: input, model, output
        module_name = node["module"]           # 예: plain_text, hf_pipeline_runner
        params = node.get("params", {})        # 추가 파라미터
        evaluator_names = node.get("evaluators", [])  # 평가기 목록

        # ✅ 실행 모듈 로딩
        module = load_module(module_type, module_name)

        # ✅ 평가기 적용 (존재 시)
        if evaluator_names:
            module = apply_evaluators(module, evaluator_names)

        # ✅ 실행 및 결과 저장
        output = module.run(input=input_data, **params)
        results[node_id] = output

    # 🔚 전체 실행 결과 반환
    return results