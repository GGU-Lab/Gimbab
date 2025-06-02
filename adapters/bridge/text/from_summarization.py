"""
📦 Bridge Adapter: from_summarization
──────────────────────────────────────────────
- 요약 결과에서 핵심 텍스트(summary_text 또는 text)를 추출하여 반환
- 후속 텍스트 기반 태스크로 넘기기 위한 정규화 Adapter

📌 입력 예시:
1. 문자열 그대로:
    "This is the summary."

2. 딕셔너리 형태:
    { "summary_text": "This is the summary." }
    { "text": "This is the summary." }

📌 출력 예시:
    { "text": "This is the summary." }
"""

from typing import Union, Dict


def run(input: Union[str, Dict], **kwargs) -> Dict[str, str]:
    """
    ✅ 요약 모델의 결과를 후속 태스크에 넘기기 위한 표준 포맷으로 변환합니다.

    Parameters
    ----------
    input : str | dict
        요약 결과 (문자열 또는 딕셔너리)
        - 문자열인 경우: 그대로 사용
        - 딕셔너리인 경우: "summary_text" → "text" → str(input) 순으로 탐색

    kwargs : dict
        확장성을 위한 키워드 인자 (현재 사용하지 않음)

    Returns
    -------
    dict
        후속 태스크로 넘길 수 있는 표준 포맷
        예: { "text": "..." }

    Raises
    ------
    ValueError
        입력이 None인 경우 예외 발생
    """

    if input is None:
        # ❌ None이 입력된 경우 명확한 예외 처리
        raise ValueError("❌ BridgeAdapter 'from_summarization'에 전달된 입력이 None입니다.")

    if isinstance(input, dict):
        # 📌 우선순위에 따라 요약 텍스트 추출
        # 1순위: summary_text
        # 2순위: text
        # 3순위: fallback → 전체 딕셔너리 문자열화
        summary = input.get("summary_text") or input.get("text") or str(input)
    else:
        # 📌 입력이 단순 문자열인 경우 그대로 사용
        summary = str(input)

    # ✅ 표준 포맷으로 반환
    return { "text": summary }
