from dataclasses import dataclass


@dataclass
class Sentence:
    start: int
    end: int
    text: str


@dataclass
class Word:
    start: int
    end: int
    text: str
    is_first: bool
    is_last: bool

    def first_is_upper(self) -> bool:
        return self.is_first and len(self.text.strip()) > 0 and self.text.strip()[0].isupper()

    def is_last_in_sentence(self):
        return self.text.strip().endswith((".", "?", "!"))
