# 📌 실행 흐름 연결 모듈
# - FastAPI 엔드포인트(main.py)에서 호출됨
# - JSON 형식으로 정의된 파이프라인(DAG)을 받아
#   실행 전 유효성 검사 후 execute_graph로 전달함

from utils.graph_executor import execute_graph


def run_pipeline_graph(pipeline_json: dict):
    """
    📌 외부 요청에서 받은 JSON DAG을 받아 실행 흐름으로 넘김
    - 입력: {"nodes": [...], "edges": [...]}
    - 출력: 실행 결과 (모든 노드 실행 후 출력 반환)

    ✅ 처리 과정 요약:
    1. JSON 구조 유효성 검사
    2. 그래프 실행기로 실행 위임
    3. 최종 결과 반환
    """

    # ✅ 필수 키 누락 여부 검사
    if "nodes" not in pipeline_json or "edges" not in pipeline_json:
        raise ValueError("Invalid pipeline format. 'nodes' and 'edges' are required.")

    # ✅ DAG 실행 (실질적 처리 로직은 graph_executor로 위임)
    result = execute_graph(
        nodes=pipeline_json["nodes"],
        edges=pipeline_json["edges"]
    )

    # 🔁 실행 결과 반환
    return result