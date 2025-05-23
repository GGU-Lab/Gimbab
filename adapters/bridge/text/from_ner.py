def run(input: list[dict], **kwargs) -> dict:
    """
    NER 출력 리스트를 받아 단일 문장(text)으로 변환합니다.
    subword(예: '##s')가 포함된 경우 앞 단어에 병합 처리합니다.
    """

    if input is None:
        raise ValueError("❌ BridgeAdapter 'from_ner'에 전달된 입력이 None입니다.")

    words = []

    for tok in input:
        word = tok.get("word", "")
        
        # '##'로 시작하면 앞 단어에 붙임 (subword 병합 처리)
        if word.startswith("##") and words:
            words[-1] += word[2:]
        else:
            words.append(word)

    # 띄어쓰기 정리 및 문장화
    sentence = " ".join(words).replace(" .", ".").replace(" ,", ",")

    return { "text": sentence }