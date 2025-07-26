import math

from ..common import Sentence, Word, Segment


class Transcriber:
    def __init__(
        self,
        term_time_ms: int,
        per_phone_ms: int,
        relocation: bool,
    ):
        self.term_time_ms = term_time_ms
        self.per_phone_ms = per_phone_ms
        self.relocation = relocation

    def transcribe(self, segments: list[Segment]) -> list[Sentence]:
        if self.relocation:
            return self.__relocate_words(segments)
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
                if self.__check_term_time(words, idx) or word.first_is_upper():
                    sentences.append(merge_words(tmp_words))
                    tmp_words = []
            tmp_words.append(word)
            if word.is_last_in_sentence():
                sentences.append(merge_words(tmp_words))
                tmp_words = []

        return sentences

    def __check_term_time(self, words: list[Word], idx: int) -> bool:
        if idx == 0:
            return False
        remaining_time = words[idx].start - words[idx - 1].end
        return remaining_time > self.term_time_ms


def merge_words(words: list[Word]) -> Sentence:
    return Sentence(
        start=words[0].start,
        end=words[-1].end,
        text=" ".join([seg.text for seg in words]).strip(),
    )
