"""
Shared utility functions.
Only Python standard library is used so it runs smoothly in Termux.
"""
import re
import sys
import datetime
from typing import List


def log(msg: str) -> None:
    """Simple stdout logger with timestamp."""
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sys.stdout.write(f"[{ts}] {msg}\n")
    sys.stdout.flush()


def normalize_text(text: str) -> str:
    """Lowercase and collapse whitespace."""
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def contains_any(text: str, keywords: List[str]) -> bool:
    text_norm = normalize_text(text)
    return any(kw.lower() in text_norm for kw in keywords)


def count_matches(text: str, keywords: List[str]) -> int:
    text_norm = normalize_text(text)
    return sum(1 for kw in keywords if kw.lower() in text_norm)
