from pathlib import Path

_CONTENT_DIR = Path(__file__).parent


def load(filename: str) -> str:
    """Load a static markdown file from the content package."""
    return (_CONTENT_DIR / filename).read_text(encoding="utf-8")
