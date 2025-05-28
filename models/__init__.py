"""
📦 Domain Dispatcher
──────────────────────────────────────────────
- 도메인(text, vision, audio, multimodal)에 따라 내부 실행기로 분기하는 공통 진입점
- 예시: domain="text", task="sentiment-analysis" → models.text.run() 호출
"""

from models.text import run as run_text
# from models.vision import run as run_vision
# from models.audio import run as run_audio
# from models.multimodal import run as run_multimodal

def run(input, task, domain="text", model_name=None, reload=False, **kwargs):
    # 📌 run(): domain에 따라 전용 실행기로 분기하여 모델 실행

    # ✅ 텍스트 도메인 실행
    if domain == "text":
        return run_text(input, task, model_name, reload, **kwargs)

    # 🔧 향후 확장을 위한 예시 코드 (주석 처리됨)
    # elif domain == "vision":
    #     return run_vision(input, task, model_name, reload, **kwargs)
    # elif domain == "audio":
    #     return run_audio(input, task, model_name, reload, **kwargs)
    # elif domain == "multimodal":
    #     return run_multimodal(input, task, model_name, reload, **kwargs)

    # ❌ 알 수 없는 도메인 입력 시 예외 처리
    else:
        raise ValueError(f"❌ Unknown model domain: {domain}")