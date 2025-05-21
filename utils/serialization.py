"""
📦 Serialization Utility: serialization.py
──────────────────────────────────────────────
- JSON 직렬화가 불가능한 타입(numpy, tensor 등)을 파이썬 기본 타입으로 변환
- FastAPI 응답이나 json.dumps 사용 전에 안전하게 변환 가능

📌 사용 예시:
from utils.serialization import to_serializable
json.dumps(to_serializable(obj))  # 또는 FastAPI 응답 전에 사용
"""

import numpy as np

# ---------------------------------------------------
# 📌 JSON 안전 변환 함수: to_serializable
# - 재귀적으로 dict, list 구조 내부를 순회하며,
#   numpy, tensor, float32 등 직렬화 불가능한 객체를
#   파이썬 기본 타입으로 변환
# ---------------------------------------------------
def to_serializable(obj):
    """
    입력 객체를 JSON 직렬화 가능한 파이썬 기본 타입으로 변환합니다.

    ✅ 변환 규칙:
    - dict: 내부 키/값 재귀 처리
    - list: 내부 항목 재귀 처리
    - numpy.int, float: item()으로 스칼라 값 추출
    - numpy.ndarray: .tolist()로 리스트 변환
    - torch.Tensor: .item() 호출 가능 시 변환
    - float subclass: float(obj) 강제 변환
    - 그 외: str(obj)로 문자열화
    """

    if isinstance(obj, dict):
        return {k: to_serializable(v) for k, v in obj.items()}
    
    elif isinstance(obj, list):
        return [to_serializable(i) for i in obj]

    # ✅ numpy 스칼라 타입 처리 (예: np.float32, np.int64 등)
    elif isinstance(obj, (np.integer, np.floating)):
        return obj.item()

    # ✅ numpy 배열 처리
    elif isinstance(obj, np.ndarray):
        return obj.tolist()

    # ✅ torch.Tensor 대응: item() 가능 시 스칼라 추출
    elif hasattr(obj, 'item') and callable(obj.item):
        try:
            return obj.item()
        except:
            pass  # fallback to str(obj) below

    # ✅ float subclass 대응 (예: np.float32 -> float)
    elif isinstance(obj, float):
        return float(obj)

    # ✅ 기타 알 수 없는 타입: 문자열로 fallback
    return str(obj)