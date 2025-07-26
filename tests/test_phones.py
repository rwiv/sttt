from phonemizer.backend import EspeakBackend

from sttt.utils import phones_for_word, set_espeak_path

set_espeak_path()


def test_phonemizer():
    print()
    backend = EspeakBackend("en-us")
    print(phones_for_word(backend, "hello world"))
