from phonemizer.backend import EspeakBackend

from sttt.utils import phones_for_word, set_espeak_path

set_espeak_path()


def test_phonemizer():
    backend = EspeakBackend("en-us")
    assert len(phones_for_word(backend, "hello world")) == 7

    backend = EspeakBackend("ko")
    assert len(phones_for_word(backend, "안녕하세요")) == 12
