def run(input: dict, **kwargs):
    """
    📦 QA 모델 결과 → 다음 모델 입력용 텍스트 변환 함수

    이 함수는 QA(Task) 모델의 출력 결과를 받아,
    그 안의 "answer" 필드를 바탕으로 다음 스텝에서 사용할 수 있는 문장 형식으로 변환합니다.

    Parameters:
    ----------
    input : dict
        QA 모델의 출력 결과 예시:
        {
            "answer": "frustrated and need help",
            "score": 0.8342
        }

    kwargs : dict
        확장성을 위한 추가 인자 (현재 사용하지 않음)

    Returns:
    -------
    dict
        변환된 출력 텍스트 형식:
        {
            "text": "The customer issue is: frustrated and need help"
        }
        만약 문제가 있거나, 유효하지 않은 경우에는 아래와 같은 포맷으로 반환:
        {
            "text": "No answer found."
        }
        또는
        {
            "text": "Invalid QA output format."
        }
        또는
        {
            "text": "[bridge.from_qa] Error: <에러 메시지>"
        }
    """
    try:
        # ✅ 입력이 딕셔너리인지 확인
        if isinstance(input, dict):
            # 🔍 "answer" 키로부터 값 추출 (없으면 기본값 "")
            answer = input.get("answer", "")
            
            # ✨ answer 값이 존재하면 포맷팅된 문장 반환
            if answer:
                return { "text": f"The customer issue is: {answer}" }
            else:
                # 🚫 answer 값이 비어있을 경우
                return { "text": "No answer found." }
        else:
            # 🚫 input이 dict가 아닌 경우 처리
            return { "text": "Invalid QA output format." }
    
    except Exception as e:
        # 🔥 예외 발생 시 에러 메시지를 포함한 텍스트 반환
        return { "text": f"[bridge.from_qa] Error: {str(e)}" }
