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


class Segment(BaseModel):
    start: int
    end: int
    text: str
    words: list[Word]
