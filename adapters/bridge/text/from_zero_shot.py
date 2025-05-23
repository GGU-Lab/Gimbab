def run(input: dict, **kwargs) -> dict:
    """
    Zero-shot classification 결과에서 가장 높은 score를 가진 label을 추출하여 text로 반환합니다.
    일반적으로 감성 분석 등 후속 태스크에 연결하기 위해 사용됩니다.
    """

    if input is None:
        raise ValueError("❌ BridgeAdapter 'from_zero_shot'에 전달된 입력이 None입니다.")

    labels = input.get("labels", [])
    scores = input.get("scores", [])

    # 필수 필드 검증
    if not labels or not scores:
        raise ValueError("❌ 'labels' 또는 'scores' 필드가 비어있습니다.")

    # 가장 높은 score를 가진 index → 해당 label 반환
    best_index = scores.index(max(scores))
    best_label = labels[best_index]

    return { "text": best_label }