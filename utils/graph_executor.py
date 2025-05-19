from typing import List, Dict, Any
from collections import defaultdict, deque
from utils.dynamic_loader import load_module
from utils.serialization import to_serializable  # ✅ 결과 직렬화용 유틸 함수

# ------------------------------------------------------
# 📌 위상 정렬 함수: 실행 순서를 결정 (선행 → 후속)
# - DAG(방향성 비순환 그래프) 기반의 노드 실행 순서를 반환
# - 사이클이 존재할 경우 실행 불가 → 예외 발생
# ------------------------------------------------------
def topological_sort(nodes: List[Dict], edges: List[Dict]) -> List[str]:
    graph = defaultdict(list)       # 노드 ID → 연결된 후속 노드 목록
    indegree = defaultdict(int)     # 노드 ID → 진입 차수 (선행 노드 개수)

    # ✅ 간선을 기반으로 그래프 구성
    for edge in edges:
        graph[edge["from"]].append(edge["to"])
        indegree[edge["to"]] += 1

    # ✅ 진입 차수가 0인 노드를 먼저 큐에 넣고 시작
    queue = deque([node["id"] for node in nodes if indegree[node["id"]] == 0])
    result = []

    # 🔁 Kahn’s Algorithm에 따라 정렬 수행
    while queue:
        current = queue.popleft()
        result.append(current)

        for neighbor in graph[current]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    # 🚨 순환이 존재하면 모든 노드를 처리하지 못하므로 오류
    if len(result) != len(nodes):
        raise ValueError("Cycle detected in DAG.")

    return result

# ------------------------------------------------------
# 📌 Evaluator 래핑 함수
# - 원본 모듈을 evaluator로 감싸서 실행 중간에 평가 기능 삽입
# - 여러 evaluator를 중첩해 사용할 수 있도록 클로저 기반 래핑
# ------------------------------------------------------
def apply_evaluators(module, evaluator_names: List[str]):
    for evaluator_name in evaluator_names:
        # 🔧 evaluator 모듈 로드 (evaluator/XXX.py)
        evaluator_module = load_module("evaluator", evaluator_name)

        # ✅ 기존 모듈을 evaluator로 감싸는 익명 클래스 생성
        def make_wrapped(prev_module, evaluator_module):
            def run(input, **params):
                # evaluator는 module=prev_module을 인자로 받음
                return evaluator_module.run(input=input, module=prev_module, **params)
            # ✅ 단일 메서드(run)를 가진 래핑 객체 반환
            return type("WrappedModule", (), {"run": staticmethod(run)})()

        module = make_wrapped(module, evaluator_module)

    return module

# ------------------------------------------------------
# 📌 전체 그래프 실행 함수: 파이프라인 핵심 실행부
# - 위상 정렬에 따라 노드를 순차 실행
# - 각 노드별 input 구성 → 모듈 로딩 → evaluator 적용 → 실행
# - 실행 결과를 노드 ID 기준으로 results에 저장
# - 최종적으로 모든 노드 결과를 직렬화 가능한 형태로 반환
# ------------------------------------------------------
def execute_graph(nodes: List[Dict[str, Any]], edges: List[Dict[str, str]]) -> Dict[str, Any]:
    node_map = {node["id"]: node for node in nodes}   # 노드 ID → 노드 정의
    edge_map = defaultdict(list)                      # 노드 ID → 입력 노드 목록

    # 🔧 edges 정보로부터 역방향 연결 정보 구성
    for edge in edges:
        edge_map[edge["to"]].append(edge["from"])

    # ✅ 노드 실행 순서 결정 (DAG 기반)
    sorted_node_ids = topological_sort(nodes, edges)

    results = {}  # 실행 결과 저장소: node_id → output

    # 🔁 노드 순차 실행
    for node_id in sorted_node_ids:
        node = node_map[node_id]
        prev_ids = edge_map[node_id]

        # 📥 입력 데이터 구성
        if len(prev_ids) == 0:
            # 시작 노드 (ex: input adapter)
            input_data = {}
        elif len(prev_ids) == 1:
            # 단일 입력은 바로 전달
            input_data = results[prev_ids[0]]
        else:
            # 다중 입력은 dict 형태로 전달
            input_data = {pid: results[pid] for pid in prev_ids}

        # ⚙️ 모듈 타입과 이름 추출 (예: model / hf_pipeline_runner)
        module_type = node["type"]
        module_name = node["module"]
        params = node.get("params", {})  # 추가 파라미터
        evaluator_names = node.get("evaluators", [])  # evaluator 목록 (옵션)

        # ✅ 실행 모듈 로딩
        module = load_module(module_type, module_name)

        # ✅ evaluator가 존재할 경우 래핑
        if evaluator_names:
            module = apply_evaluators(module, evaluator_names)

        # ▶️ 실행 및 결과 저장
        output = module.run(input=input_data, **params)
        results[node_id] = output

    # ✅ 전체 실행 결과를 JSON 직렬화 가능한 형태로 변환 후 반환
    return to_serializable(results)