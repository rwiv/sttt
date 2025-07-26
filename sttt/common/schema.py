from pydantic import BaseModel


class Sentence(BaseModel):
    start: int
    end: int
    text: str


class Word(BaseModel):
    start: int
    end: int
    text: str
    is_first: bool
    is_last: bool
    score: float

    def first_is_upper(self) -> bool:
        return self.is_first and len(self.text.strip()) > 0 and self.text.strip()[0].isupper()

    def is_last_in_sentence(self):
        return self.text.strip().endswith((".", "?", "!"))


class Segment(BaseModel):
    start: int
    end: int
    text: str
    words: list[Word]
