"""
📦 Graph Executor: graph_executor.py
──────────────────────────────────────────────
- JSON 기반 파이프라인 정의(nodes + edges)를 받아
  위상 정렬 → 노드별 모듈 로딩 → evaluator 래핑 → 실행 → 결과 저장
  의 전체 흐름을 담당하는 실행 엔진입니다.

- 최종 결과는 모든 노드 ID → 실행 결과 형태의 dict이며,
  JSON 직렬화 가능한 형태로 반환됩니다.
"""

from typing import List, Dict, Any
from collections import defaultdict, deque
from utils.dynamic_loader import load_module
from utils.serialization import to_serializable
from utils.evaluator_runner import apply_evaluators  

# ------------------------------------------------------
# 📌 위상 정렬 함수: 실행 순서를 결정 (선행 → 후속)
# - DAG(방향성 비순환 그래프) 구조를 기반으로 노드 실행 순서를 계산합니다.
# - 순환(cycle)이 감지될 경우 예외 발생
# ------------------------------------------------------
def topological_sort(nodes: List[Dict], edges: List[Dict]) -> List[str]:
    graph = defaultdict(list)      # 노드 → 후속 노드 목록
    indegree = defaultdict(int)    # 노드 → 진입 차수(선행 노드 수)

    # ✅ 간선을 기반으로 연결 관계 및 진입 차수 계산
    for edge in edges:
        graph[edge["from"]].append(edge["to"])
        indegree[edge["to"]] += 1

    # ✅ 진입 차수가 0인 노드를 큐에 추가 (시작 노드 후보)
    queue = deque([node["id"] for node in nodes if indegree[node["id"]] == 0])
    result = []

    # 🔁 Kahn’s Algorithm 기반 위상 정렬 수행
    while queue:
        current = queue.popleft()
        result.append(current)

        for neighbor in graph[current]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    # 🚨 모든 노드가 정렬되지 못한 경우 → 순환 발생
    if len(result) != len(nodes):
        raise ValueError("Cycle detected in DAG.")

    return result

# ------------------------------------------------------
# 📌 전체 그래프 실행 함수: 파이프라인 실행 핵심
# - 입력 노드부터 시작해 각 노드를 위상 정렬 순서대로 실행
# - 각 노드는 모듈 로딩 → evaluator 래핑(옵션) → run(input, **params)
# - 결과는 results[node_id]에 저장됨
# - 최종적으로 모든 결과를 직렬화 가능한 형태로 반환
# ------------------------------------------------------
def execute_graph(nodes: List[Dict[str, Any]], edges: List[Dict[str, str]]) -> Dict[str, Any]:
    # ✅ 노드 ID → 노드 정의 매핑
    node_map = {node["id"]: node for node in nodes}

    # ✅ 노드 ID → 연결된 선행 노드 목록 구성
    edge_map = defaultdict(list)
    for edge in edges:
        edge_map[edge["to"]].append(edge["from"])

    # ✅ DAG 기반 위상 정렬로 실행 순서 계산
    sorted_node_ids = topological_sort(nodes, edges)

    # ✅ 노드 실행 결과 저장소
    results = {}

    # 🔁 위상 정렬 순서에 따라 각 노드 실행
    for node_id in sorted_node_ids:
        node = node_map[node_id]
        prev_ids = edge_map[node_id]

        # 📥 입력 데이터 구성: 선행 노드들의 실행 결과 활용
        if len(prev_ids) == 0:
            input_data = {}  # 시작 노드 (ex: input adapter)
        elif len(prev_ids) == 1:
            input_data = results[prev_ids[0]]  # 단일 입력이면 바로 전달
        else:
            input_data = {pid: results[pid] for pid in prev_ids}  # 다중 입력 → dict 구조

        # ⚙️ 모듈 타입 및 이름 추출
        module_type = node["type"]               # 예: input, model, output
        module_name = node["module"]             # 예: plain_text, hf_pipeline_runner
        params = node.get("params", {})          # 추가 파라미터
        evaluator_names = node.get("evaluators", [])  # 평가기 이름 리스트 (선택)

        # ✅ 실행 모듈 로딩 (동적 import)
        module = load_module(module_type, module_name)

        # ✅ 평가기가 존재하면 evaluator 래퍼로 감쌈
        if evaluator_names:
            module = apply_evaluators(module, evaluator_names)

        # ▶️ 노드 실행 및 결과 저장
        output = module.run(input=input_data, **params)
        results[node_id] = output

    # 📤 실행 결과를 JSON 직렬화 가능한 형태로 반환
    return to_serializable(results)