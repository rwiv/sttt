from phonemizer.backend import EspeakBackend

from ..common import Sentence, Word, Segment
from ..utils import phones_for_word


class Transcriber:
    def __init__(
        self,
        phone_backend: EspeakBackend,
        silence_threshold_ms: int,
        seg_relocation: bool,
        phones_check: bool,
        phones_per_ms: int,
    ):
        self.__phone_backend = phone_backend
        self.__silence_threshold_ms = silence_threshold_ms
        self.__seg_relocation = seg_relocation
        self.__phones_check = phones_check
        self.__phones_per_ms = phones_per_ms

    def transcribe(self, segments: list[Segment]) -> list[Sentence]:
        if self.__seg_relocation:
            return self.__relocate_words(segments)
        else:
            return [Sentence(start=s.start, end=s.end, text=s.text.strip()) for s in segments]

    def __relocate_words(self, segments: list[Segment]) -> list[Sentence]:
        words = []
        for seg in segments:
            for word in seg.words:
                words.append(word)

        if len(words) == 0:
            raise ValueError("No words found in the audio")

        sentences: list[Sentence] = []
        tmp_words: list[Word] = []
        for idx, word in enumerate(words):
            if len(tmp_words) > 0:
                if word.is_first or self.__check_silence(words, idx, True):
                    sentences.append(merge_words(tmp_words))
                    tmp_words = []
                elif self.__phones_check and self.__check_silence_by_phones(words, idx):
                    sentences.append(merge_words(tmp_words))
                    tmp_words = []

            tmp_words.append(word)

            if word.check_last() or self.__check_silence(words, idx, False):
                sentences.append(merge_words(tmp_words))
                tmp_words = []

        return sentences

    def __check_silence_by_phones(self, words: list[Word], idx: int) -> bool:
        """
        현재 word와 이전 word 사이 빈 시간이 term_time_ms를 초과하는지 체크하는 함수.
        최초 sentence인지 체크하기 위한 목적으로 사용한다.
        whisper는 전사한 sentence 앞/뒤에 빈 시간을 포함할 수 있기에 단순히 cur.start - prev.end로 단어 간 대기 시간을 체크할 수 없다.
        따라서 예상 발음 시간을 구한 뒤 `cur.end - prev.end - 예상 발음 시간`을 통해 대기 시간을 추정한다.
        문장 마지막 단어의 경우 후미에 빈 시간이 포함될 수 있기에 스킵한다.
        |-e-|-p-|-e-|   (0~?ms)   |-e-|-p-|-e-|
        """
        cur = words[idx]
        if idx == 0 or cur.check_last():
            return False

        phones = phones_for_word(self.__phone_backend, cur.text.strip())
        est_pron_time = len(phones) * self.__phones_per_ms
        remaining_time = cur.end - words[idx - 1].end - est_pron_time
        return remaining_time > self.__silence_threshold_ms

    def __check_silence(self, words: list[Word], idx: int, is_first: bool) -> bool:
        cur = words[idx]
        last_idx = len(words) - 1
        if idx == 0:
            return False

        if is_first:
            if cur.check_last():
                return False
            prev = words[idx - 1]
            return cur.start - prev.end > self.__silence_threshold_ms
        else:
            if cur.is_first:
                return False
            if idx == last_idx:
                return True
            nxt = words[idx + 1]
            return nxt.start - cur.end > self.__silence_threshold_ms


def merge_words(words: list[Word]) -> Sentence:
    return Sentence(
        start=words[0].start,
        end=words[-1].end,
        text=" ".join([seg.text for seg in words]).strip(),
    )
