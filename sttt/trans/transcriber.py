import math

from phonemizer.backend import EspeakBackend

from ..common import Sentence, Word, Segment
from ..utils import phones_for_word


class Transcriber:
    def __init__(
        self,
        phone_backend: EspeakBackend,
        term_time_ms: int,
        per_phone_ms: int,
        relocation: bool,
    ):
        self.phone_backend = phone_backend
        self.term_time_ms = term_time_ms
        self.per_phone_ms = per_phone_ms
        self.relocation = relocation

    def transcribe(self, segments: list[Segment]) -> list[Sentence]:
        if self.relocation:
            return self._relocate_words(segments)
        else:
            result = []
            for seg in segments:
                sentence = Sentence(
                    start=math.floor(seg.start * 1000),
                    end=math.floor(seg.end * 1000),
                    text=seg.text.strip(),
                )
                result.append(sentence)
            return result

    def _relocate_words(self, segments: list[Segment]) -> list[Sentence]:
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
                if self._check_term_time(words, idx) or word.first_is_upper():
                    sentences.append(merge_words(tmp_words))
                    tmp_words = []
            tmp_words.append(word)
            if word.is_last_in_sentence():
                sentences.append(merge_words(tmp_words))
                tmp_words = []

        return sentences

    # 현재 word와 이전 word 사이 빈 시간이 term_time_ms를 초과하는지 체크. 최초 sentence인지 체크하기 위한 목적으로 사용
    # whisper는 전사한 sentence 앞에 empty_time을 포함하기 때문에 단순히 cur.start - prev.end로 빈 시간을 체크할 수 없음
    # 따라서 예상 발음 시간을 구한 뒤 `cur.end - prev.end - 예상 발음 시간`을 통해 빈 시간을 체크
    # |--empty_time--|--pronunciation_time--|   (0~?ms)   |--empty_time--|--pronunciation_time--|
    def _check_term_time(self, words: list[Word], idx: int) -> bool:
        if idx == 0:
            return False
        phones = phones_for_word(self.phone_backend, words[idx].text.strip())
        est_pron_time = len(phones) * self.per_phone_ms
        remaining_time = words[idx].end - words[idx - 1].end - est_pron_time
        return remaining_time > self.term_time_ms


def merge_words(words: list[Word]) -> Sentence:
    return Sentence(
        start=words[0].start,
        end=words[-1].end,
        text=" ".join([seg.text for seg in words]).strip(),
    )
