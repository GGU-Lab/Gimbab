from .plain_text import run as plain_text
from .zero_shot_input import run as zero_shot_input
from .qa_input import run as qa_input
from .fill_mask_input import run as fill_mask_input
from .summarization_input import run as summarization_input
from .text2text_input import run as text2text_input

__all__ = [
    "plain_text",
    "zero_shot_input",
    "qa_input",
    "fill_mask_input",
    "summarization_input",
    "text2text_input"
]