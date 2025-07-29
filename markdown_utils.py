import re

def normalize_punctuation(text: str) -> str:
    """
    Replace common unicode punctuation with ASCII equivalents.
    """
    punct_map = {
        "‘": "'",
        "’": "'",
        "“": '"',
        "”": '"',
        "–": '-',
        "—": '-',
        "…": '...'
    }
    for k, v in punct_map.items():
        text = text.replace(k, v)
    return text

def strip_inline_bold(text: str) -> str:
    """
    Remove inline formatting, bold markers, trailing numbers, repeated punctuation, and normalize whitespace.
    """
    text = normalize_punctuation(text)
    text = re.sub(r'`([^`]+)`', r"\1", text)  # Remove code backticks
    text = text.replace('`', '')                # Remove stray backticks
    text = re.sub(r'_?\*\*(.*?)\*\*_?', r"\1", text)  # Remove bold
    text = re.sub(r'(?:\b)(\d+)$', '', text)  # Remove trailing numbers
    text = re.sub(r'[\.\-\,\"\=]{2,}', '', text)  # Remove repeated punctuation
    return ' '.join(text.split()).strip()
