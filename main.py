# 📌 FastAPI 기반 백엔드 서버 정의
# - 클라이언트로부터 JSON 형식의 파이프라인 실행 요청을 받음
# - pipeline_graph_runner.py를 통해 실행 로직을 위임
# - 결과를 JSON 형식으로 반환
# uvicorn main:app --reload

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, Any

# 📌 파이프라인 실행 로직을 외부 모듈로 분리하여 호출
from pipeline_graph_runner import run_pipeline_graph

# ✅ FastAPI 애플리케이션 인스턴스 생성
app = FastAPI()

# -----------------------------------------
# 📌 입력 요청 바디 구조 정의
# - 클라이언트는 nodes와 edges 리스트를 포함한 JSON을 POST로 전달해야 함
# - 예시 입력:
#   {
#       "nodes": [...],
#       "edges": [...]
#   }
# -----------------------------------------
class PipelineRequest(BaseModel):
    nodes: list
    edges: list

# -----------------------------------------
# ✅ 실행 API 엔드포인트
# POST /pipeline/graph/run
# - JSON 요청을 받아 실행 로직으로 전달
# - 결과를 성공/실패 여부와 함께 JSON으로 응답
# -----------------------------------------
@app.post("/pipeline/graph/run")
async def run_pipeline(request: PipelineRequest):
    try:
        # 🔄 파이프라인 실행 함수 호출 (JSON → dict 변환하여 전달)
        result = run_pipeline_graph(request.dict())
        
        # ✅ 정상 실행 결과 반환
        return JSONResponse(content={"status": "success", "result": result})
    
    except Exception as e:
        # 🚨 실행 중 예외 발생 시 에러 메시지 반환
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})