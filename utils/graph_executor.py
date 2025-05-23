from typing import List, Dict, Any
from collections import defaultdict, deque
from utils.dynamic_loader import load_module
from utils.serialization import to_serializable
from utils.evaluator_runner import apply_evaluators

# ------------------------------------------------------
# 📌 위상 정렬 함수
# - 노드 목록과 간선 목록(DAG)을 입력으로 받아
# - 노드 실행 순서를 위상 정렬 순서로 반환
# - 순환(cycle) 구조가 감지되면 예외 발생
# ------------------------------------------------------
def topological_sort(nodes: List[Dict], edges: List[Dict]) -> List[str]:
    graph = defaultdict(list)      # 노드 ID → 후속 노드 ID 리스트
    indegree = defaultdict(int)    # 노드 ID → 진입 차수 (선행 노드 수)

    # ✅ 간선을 기반으로 그래프와 진입 차수 정보 구성
    for edge in edges:
        graph[edge["from"]].append(edge["to"])
        indegree[edge["to"]] += 1

    # ✅ 진입 차수가 0인 노드(시작점)부터 탐색 시작
    queue = deque([node["id"] for node in nodes if indegree[node["id"]] == 0])
    result = []

    # 🔁 Kahn’s Algorithm을 사용한 위상 정렬
    while queue:
        current = queue.popleft()
        result.append(current)

        for neighbor in graph[current]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    # 🚨 모든 노드가 정렬되지 못하면 순환 구조 존재
    if len(result) != len(nodes):
        raise ValueError("Cycle detected in DAG.")

    return result

# ------------------------------------------------------
# 📌 전체 파이프라인 실행 함수
# - JSON으로 정의된 DAG 파이프라인을 받아
#   노드들을 위상 정렬 순으로 실행함
# - 각 노드는 input 구성 → 모듈 로딩 → evaluator 래핑 → run 실행
# - 실행 결과는 노드 ID를 key로 하는 dict에 저장
# ------------------------------------------------------
def execute_graph(nodes: List[Dict[str, Any]], edges: List[Dict[str, str]]) -> Dict[str, Any]:
    # ✅ 노드 ID → 노드 정보 매핑
    node_map = {node["id"]: node for node in nodes}

    # ✅ 노드 ID → 선행 노드 ID 리스트 구성
    edge_map = defaultdict(list)
    for edge in edges:
        edge_map[edge["to"]].append(edge["from"])

    # ✅ 위상 정렬로 노드 실행 순서 결정
    sorted_node_ids = topological_sort(nodes, edges)

    # ✅ 각 노드의 실행 결과를 저장할 딕셔너리
    results = {}

    # 🔁 정렬된 순서에 따라 노드 실행
    for node_id in sorted_node_ids:
        node = node_map[node_id]
        prev_ids = edge_map[node_id]

        # 📥 선행 노드 결과 기반으로 input 구성
        if len(prev_ids) == 0:
            input_data = {}  # 입력 노드 (input type)
        elif len(prev_ids) == 1:
            input_data = results[prev_ids[0]]  # 단일 선행 노드 결과
        else:
            input_data = {pid: results[pid] for pid in prev_ids}  # 여러 선행 노드 결과 병합

        # 📦 노드 실행 정보 추출
        module_type = node["type"]              # 예: "input", "model", "bridge", "output"
        module_name = node["module"]            # 모듈 이름
        params = node.get("params", {})         # 실행 파라미터
        evaluator_names = node.get("evaluators", [])  # 평가 모듈 이름 리스트

        # ✅ 모듈 로딩 방식 분기
        if module_type == "bridge":
            # 브릿지 어댑터는 adapters.bridge 패키지 아래 직접 import
            from importlib import import_module
            bridge_module = import_module(f"adapters.bridge.{module_name}")
            module = bridge_module
        else:
            # input/model/output은 공통 로더 사용
            module = load_module(module_type, module_name)

        # ✅ evaluator가 존재하면 래핑
        if evaluator_names:
            module = apply_evaluators(module, evaluator_names)

        # ▶️ 실제 노드 실행
        output = module.run(input=input_data, **params)

        # 📌 결과 저장 (노드 ID 기준)
        results[node_id] = output

    # 📤 전체 결과를 직렬화 가능한 형식으로 반환
    return to_serializable(results)