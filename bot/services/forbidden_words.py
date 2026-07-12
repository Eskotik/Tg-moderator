import json
import re

from bot.config import FORBIDDEN_WORDS_PATH


def load_forbidden_words() -> list[str]:
    with open(FORBIDDEN_WORDS_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


forbidden_words = load_forbidden_words()


def contains_forbidden_word(message_text: str) -> bool:
    text_words = set(re.split(r"\W+", message_text.lower()))
    for phrase in forbidden_words:
        phrase_words = set(re.split(r"\W+", phrase.lower()))
        if phrase_words.issubset(text_words) or re.search(
            rf"{phrase}[?!,.@#*&^:;()$]?", message_text, re.IGNORECASE
        ):
            return True
    return False
