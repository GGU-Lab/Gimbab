def run(input: list | dict | str, **kwargs) -> dict:
    """
    번역 결과에서 'translation_text' 필드를 추출하여 하나의 문장으로 반환합니다.
    리스트의 경우 여러 문장을 합칩니다.
    """

    if isinstance(input, list):
        # 리스트일 경우 각 dict에서 translation_text를 추출
        texts = [i.get("translation_text", str(i)) for i in input]
        return { "text": " ".join(texts) }

    if isinstance(input, dict):
        # 단일 dict → 해당 필드 추출
        return { "text": input.get("translation_text", str(input)) }

    # 그 외: str 등 직접 반환
    return { "text": str(input) }