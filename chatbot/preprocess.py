"""
preprocess.py
--------------
Text preprocessing utilities for the SafeX FAQ Chatbot.

Cleaning user input before matching helps the model focus on meaningful
words rather than punctuation, casing, or extra whitespace.
"""

import re


def clean_text(text: str) -> str:
    """
    Lowercase the text, strip punctuation/special characters, and
    collapse extra whitespace. Returns a clean string ready for
    vectorization.
    """
    if not isinstance(text, str):
        return ""

    text = text.lower()
    # Keep letters, numbers, and spaces only
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    # Collapse multiple spaces into one
    text = re.sub(r"\s+", " ", text).strip()
    return text


def clean_series(texts):
    """Apply clean_text to a list/Series of strings."""
    return [clean_text(t) for t in texts]
