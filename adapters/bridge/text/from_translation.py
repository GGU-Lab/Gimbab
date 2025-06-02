def run(input: list | dict | str, **kwargs) -> dict:
    """
    📦 Bridge Adapter: from_translation
    ──────────────────────────────────────────────
    번역 결과에서 핵심 번역 텍스트(`translation_text`)를 추출하여
    후속 모델에 넘길 수 있는 단일 문장 형태로 정제합니다.

    ✅ 입력 형태:
    - 단일 문자열(str)
    - 단일 결과 딕셔너리(dict): {"translation_text": "..."}
    - 여러 번역 결과의 리스트(list[dict]): [{"translation_text": "..."}, ...]

    ✅ 출력 형태:
    - { "text": "..." } 형식의 단일 문장 반환

    Parameters
    ----------
    input : list | dict | str
        번역 결과. 번역기 모델에 따라 다양한 형태로 반환될 수 있음.

    kwargs : dict
        확장성 확보를 위한 추가 인자 (현재 사용되지 않음)

    Returns
    -------
    dict
        정제된 번역 결과:
        {
            "text": "This is the translated sentence."
        }
    """

    if isinstance(input, list):
        # 📚 여러 문장이 리스트 형태로 전달된 경우
        # 각 항목에서 'translation_text' 키를 추출하거나 fallback으로 문자열 처리
        texts = [i.get("translation_text", str(i)) for i in input]
        # 🔗 공백으로 연결해 하나의 문장으로 변환
        return { "text": " ".join(texts) }

    if isinstance(input, dict):
        # 🧩 단일 딕셔너리일 경우 'translation_text' 필드 우선 추출
        return { "text": input.get("translation_text", str(input)) }

    # ✨ 그 외: 문자열 등은 그대로 사용
    return { "text": str(input) }