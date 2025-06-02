def run(input: list[dict], **kwargs) -> dict:
    """
    📦 NER 모델의 출력 리스트를 받아 하나의 자연어 문장(text)으로 변환합니다.

    - 일반적으로 NER 모델은 토큰 단위의 출력 리스트를 반환하며,
      각 항목은 {"word": str, "entity": str, "score": float, ...} 형태로 구성됩니다.

    - 이 함수는 그 중 "word" 필드를 추출하여 문장을 재구성합니다.
    - subword 토큰(예: "##ing")이 존재하는 경우, 앞 단어에 병합하여 자연스러운 단어 형태를 유지합니다.

    Parameters
    ----------
    input : list[dict]
        NER 모델의 출력 리스트 (예: HuggingFace token-classification pipeline 결과)
        예시:
        [
            {"word": "Sam", "entity": "B-PER", ...},
            {"word": "##sung", "entity": "I-PER", ...},
            {"word": "is", ...},
            {"word": "great", ...},
            {"word": ".", ...}
        ]

    kwargs : dict
        확장성을 위한 키워드 인자 (현재는 사용하지 않음)

    Returns
    -------
    dict
        병합 및 정제된 자연어 문장:
        {
            "text": "Samsung is great."
        }

    Raises
    ------
    ValueError
        input이 None인 경우 명시적 예외 발생
    """

    if input is None:
        raise ValueError("❌ BridgeAdapter 'from_ner'에 전달된 입력이 None입니다.")

    words = []  # 👉 최종 단어 리스트 (문장 조합에 사용)

    for tok in input:
        word = tok.get("word", "")  # ⛏ word 필드만 추출

        # ✅ Subword 토큰 처리: '##'로 시작하면 앞 단어에 병합
        if word.startswith("##") and words:
            # 기존 마지막 단어에 현재 subword를 붙여줌
            words[-1] += word[2:]
        else:
            # 일반 토큰이면 그대로 추가
            words.append(word)

    # 🔧 띄어쓰기 후속 정리:
    # - " ." → "." / " ," → "," 등 불필요한 공백 제거
    sentence = " ".join(words).replace(" .", ".").replace(" ,", ",")

    return { "text": sentence }
