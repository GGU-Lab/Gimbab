def run(input: dict, **kwargs):
    """
    📌 sentiment-analysis 결과 → 문장 딕셔너리로 반환

    이 함수는 감정 분석 모델(예: HuggingFace의 `pipeline("sentiment-analysis")`)의 결과를 받아,
    가장 첫 번째 예측 결과를 기반으로 `"text"` 키를 가진 딕셔너리로 변환합니다.

    Parameters
    ----------
    input : dict
        예측 결과 리스트 (리스트 형태지만 dict로 감싸서 들어오는 경우를 허용)
        예시:
        [
            {
                "label": "POSITIVE",
                "score": 0.9876
            }
        ]

    kwargs : dict
        확장성을 위한 추가 인자 (현재 사용하지 않음)

    Returns
    -------
    dict
        변환된 감정 설명 문장:
        {
            "text": "The sentiment of the user is positive."
        }

        오류 또는 예외 발생 시 에러 메시지를 담은 문장 반환:
        {
            "text": "[bridge.from_sentiment] Error: ..."
        }
    """
    try:
        predictions = input  # 입력을 그대로 predictions로 할당

        # ✅ 입력이 리스트인지 확인 (예: [ {"label": "...", "score": ...}, ... ])
        if not isinstance(predictions, list):
            return { "text": "[bridge.from_sentiment] Error: input is not a list" }

        # 📭 예측 결과가 비어있다면 처리 불가
        if len(predictions) == 0:
            return { "text": "No sentiment detected." }

        first = predictions[0]  # 첫 번째 예측 결과만 사용

        # ✅ 첫 번째 항목이 딕셔너리인 경우 label 추출
        if isinstance(first, dict):
            label = first.get("label", "").lower()  # 감정 라벨을 소문자로 변환
            return { "text": f"The sentiment of the user is {label}." }
        else:
            # 📛 리스트의 첫 항목이 dict가 아닐 경우 예외 처리
            return { "text": "[bridge.from_sentiment] Error: First item in list is not a dict" }

    except Exception as e:
        # 🔥 예외 발생 시 에러 메시지를 포함해 반환
        return { "text": f"[bridge.from_sentiment] Error: {str(e)}" }