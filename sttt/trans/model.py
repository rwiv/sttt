from typing import BinaryIO, Iterable

from faster_whisper import WhisperModel
from faster_whisper.transcribe import Segment
from numpy import ndarray
from pyutils import log

device = "cuda"
word_timestamps = True


class SttModel:
    def __init__(self, model_size: str, compute_type: str):
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)
        log.info(f"Model loaded: {model_size}")

    def transcribe(self, file: str | BinaryIO | ndarray) -> list[Segment]:
        segments, info = self.model.transcribe(file, language="en", word_timestamps=word_timestamps)
        result = []
        for seg in segments:
            result.append(seg)
        return result
