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

    def check_last(self):
        return self.is_last or self.exists_last_prefix()

    def exists_last_prefix(self):
        return self.text.strip().endswith((".", "?", "!"))


class Segment(BaseModel):
    start: int
    end: int
    text: str
    words: list[Word]
