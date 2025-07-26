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
                if word.is_first or self.__check_term_time(words, idx):
                    sentences.append(merge_words(tmp_words))
                    tmp_words = []

            tmp_words.append(word)

            if word.is_last or word.text.strip().endswith((".", "?", "!")):
                sentences.append(merge_words(tmp_words))
                tmp_words = []

        return sentences

    def __check_term_time(self, words: list[Word], idx: int) -> bool:
        """
        현재 word와 이전 word 사이 빈 시간이 term_time_ms를 초과하는지 체크하는 함수.
        최초 sentence인지 체크하기 위한 목적으로 사용한다.
        whisper는 전사한 sentence 앞에 empty_time을 포함할 수 있기에 단순히 cur.start - prev.end로 단어 간 대기 시간을 체크할 수 없다
        따라서 예상 발음 시간을 구한 뒤 `cur.end - prev.end - 예상 발음 시간`을 통해 대기 시간을 추정한다
        |-e-|-p-|-e-|   (0~?ms)   |-e-|-p-|-e-|
        """
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
