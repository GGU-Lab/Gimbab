def run(input: dict, **kwargs) -> dict:
    """
    📦 Bridge Adapter: from_zero_shot
    ────────────────────────────────────────────────
    Zero-shot classification 모델의 출력 결과로부터
    가장 높은 score를 가진 label을 추출하여 텍스트로 반환합니다.

    이 어댑터는 주로 감정 분류, 주제 분류 등 다중 후보 레이블 중
    가장 적합한 단일 레이블을 후속 태스크에 넘길 때 사용됩니다.

    ✅ 입력 예시:
    {
        "labels": ["positive", "neutral", "negative"],
        "scores": [0.12, 0.07, 0.81]
    }

    ✅ 출력 예시:
    {
        "text": "negative"
    }

    Parameters
    ----------
    input : dict
        Zero-shot 분류 결과. 반드시 "labels"와 "scores" 키를 포함해야 함.
        - labels: 후보 레이블 리스트 (str[])
        - scores: 해당 레이블의 점수 리스트 (float[])

    kwargs : dict
        확장성을 위한 키워드 인자 (현재 사용되지 않음)

    Returns
    -------
    dict
        가장 높은 점수를 받은 레이블을 포함한 딕셔너리
        {
            "text": "best_label"
        }

    Raises
    ------
    ValueError
        입력이 None이거나 필수 필드가 비어있는 경우
    """

    if input is None:
        # 🚫 None 입력에 대한 예외 처리
        raise ValueError("❌ BridgeAdapter 'from_zero_shot'에 전달된 입력이 None입니다.")

    # 🔍 입력에서 레이블과 점수 리스트 추출
    labels = input.get("labels", [])
    scores = input.get("scores", [])

    # ✅ 필수 필드 확인: 둘 중 하나라도 비어 있으면 오류
    if not labels or not scores:
        raise ValueError("❌ 'labels' 또는 'scores' 필드가 비어있습니다.")

    # 🎯 최고 점수를 가진 인덱스를 찾아 해당 레이블 선택
    best_index = scores.index(max(scores))
    best_label = labels[best_index]

    # ✅ 후속 처리용 표준 포맷으로 반환
    return { "text": best_label }