import os

from phonemizer.backend import EspeakBackend
from phonemizer.backend.espeak.wrapper import EspeakWrapper
from phonemizer.punctuation import Punctuation
from phonemizer.separator import Separator
from phonemizer.utils import str2list

punctuation = Punctuation(';:,.!"?()-')
separator = Separator(phone=" ", word=None)  # type: ignore


def phones_for_word(backend: EspeakBackend, word: str) -> list[str]:
    text = punctuation.remove(word.lower())
    text = [line.strip(os.linesep) for line in str2list(text)]
    text = [line for line in text if line.strip()]
    phones = backend.phonemize(text, separator=separator, strip=True)
    if len(phones) != 1:
        raise ValueError(f"Invalid output length: {phones}")
    return phones[0].split(" ")


def set_espeak_path():
    EspeakWrapper.set_library("C:\\Program Files\\eSpeak NG\\libespeak-ng.dll")
