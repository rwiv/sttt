from sttt.utils.phones import phones_for_word, set_espeak_path

set_espeak_path()


def test_phonemizer():
    print()
    print(phones_for_word("hello world"))
