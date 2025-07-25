from phonemizer import phonemize
from phonemizer.backend.espeak.wrapper import EspeakWrapper
from phonemizer.punctuation import Punctuation
from phonemizer.separator import Separator


def phones_for_word(word: str):
    text = Punctuation(';:,.!"?()-').remove(word.lower())
    separator = Separator(phone=" ", word=None)  # type: ignore
    p = phonemize(
        text, language="en-us", backend="espeak", separator=separator, strip=True
    )
    if not isinstance(p, str):
        raise ValueError(f"Invalid output type: {p}")
    return p.split(" ")


def set_espeak_path():
    EspeakWrapper.set_library("C:\\Program Files\\eSpeak NG\\libespeak-ng.dll")
