from typing import List, Dict, Any
from collections import defaultdict, deque
from utils.dynamic_loader import load_module
from utils.serialization import to_serializable
from utils.evaluator_runner import apply_evaluators

# ------------------------------------------------------
# 📦 DAG 유틸리티: 위상 정렬
# ------------------------------------------------------
def topological_sort(nodes: List[Dict], edges: List[Dict]) -> List[str]:
    """
    ✅ DAG 형태의 노드/엣지 정의로부터 실행 순서를 정렬

    - 노드: 각 실행 유닛 (id 포함)
    - 엣지: "from" → "to" 구조
    - 반환값: 실행 가능한 순서대로 정렬된 노드 id 리스트

    🚨 순환 참조가 존재할 경우 예외 발생
    """
    graph = defaultdict(list)
    indegree = defaultdict(int)

    # 🔄 그래프 구조 및 진입 차수 계산
    for edge in edges:
        graph[edge["from"]].append(edge["to"])
        indegree[edge["to"]] += 1

    # ✅ 진입 차수가 0인 노드부터 큐에 삽입
    queue = deque([node["id"] for node in nodes if indegree[node["id"]] == 0])
    result = []

    # 🔁 위상 정렬 수행 (Kahn's Algorithm)
    while queue:
        current = queue.popleft()
        result.append(current)

        for neighbor in graph[current]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    # 🚨 순환 참조 감지
    if len(result) != len(nodes):
        raise ValueError("Cycle detected in DAG.")

    return result

# ------------------------------------------------------
# 📦 DAG 실행 엔진: 그래프 실행
# ------------------------------------------------------
def execute_graph(nodes: List[Dict[str, Any]], edges: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    ✅ 정의된 노드/엣지 DAG를 기반으로 전체 파이프라인 실행

    - 노드: 실행 단위 (모듈 정보, 입력, 파라미터 등 포함)
    - 엣지: 노드 간 연결 관계
    - 결과: 모든 노드의 실행 결과 dict (id → 출력)

    특이사항:
    - 모델 실행 시 domain 보정
    - bridge adapter는 별도 import 처리
    - 다중 입력은 dict로 묶어서 전달
    - evaluator 지정 시 래핑
    """
    node_map = {node["id"]: node for node in nodes}
    edge_map = defaultdict(list)

    # 📥 역방향 엣지 매핑 (to → from 리스트)
    for edge in edges:
        edge_map[edge["to"]].append(edge["from"])

    # 🔁 실행 순서 정렬
    sorted_node_ids = topological_sort(nodes, edges)
    results = {}

    for node_id in sorted_node_ids:
        node = node_map[node_id]
        prev_ids = edge_map[node_id]

        # 📥 입력 구성: 이전 노드들의 결과
        if len(prev_ids) == 0:
            input_data = {}
        elif len(prev_ids) == 1:
            input_data = results[prev_ids[0]]
        else:
            input_data = {pid: results[pid] for pid in prev_ids}

        module_type = node["type"]
        module_name = node["module"]
        params = node.get("params", {})
        evaluator_names = node.get("evaluators", [])

        # ✅ BridgeAdapter는 별도 import 처리 (직접 지정된 경로)
        if module_type == "bridge":
            from importlib import import_module
            bridge_module = import_module(f"adapters.bridge.{module_name}")
            module = bridge_module
        else:
            # 📦 일반 모듈 로딩
            module = load_module(module_type, module_name)

        # ✅ 모델 모듈인 경우 domain 누락 시 기본값 보정
        if module_type == "model":
            domain = params.get("domain", "text")
            params["domain"] = domain

        # ✅ evaluator 존재 시 래핑 적용
        if evaluator_names:
            module = apply_evaluators(module, evaluator_names)

        # 🧠 모듈 실행
        output = module.run(input=input_data, **params)
        results[node_id] = output

    # 📤 전체 결과 JSON 직렬화 변환 후 반환
    return to_serializable(results)