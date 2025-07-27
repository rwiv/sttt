import gc
import math
from abc import ABC, abstractmethod

import torch
import whisperx
from faster_whisper import WhisperModel, BatchedInferencePipeline
from pyutils import log

from ..common import Word, Segment

CUDA_DEVICE = "cuda"
VAD_MIN_SILENCE_MS = 1000


class SttModel(ABC):
    @abstractmethod
    def transcribe(self, audio_file_path: str, language: str) -> list[Segment]:
        pass


class SttModelFasterWhisper(SttModel):
    def __init__(self, model_size: str, compute_type: str, batch_size: int):
        self.__model_size = model_size
        self.__compute_type = compute_type
        self.__batch_size = batch_size

    def transcribe(self, audio_file_path: str, language: str) -> list[Segment]:
        model = WhisperModel(self.__model_size, compute_type=self.__compute_type, device=CUDA_DEVICE)
        batched_model = BatchedInferencePipeline(model=model)
        log.info("Load model")
        raw_segments, _ = batched_model.transcribe(
            audio=audio_file_path,
            language=language,
            batch_size=self.__batch_size,
            word_timestamps=True,
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=VAD_MIN_SILENCE_MS),
        )
        segments = []
        for raw_seg in raw_segments:
            raw_words = raw_seg.words
            if raw_words is None:
                raise ValueError("No words found in the audio")
            words = []
            for idx, raw_word in enumerate(raw_words):
                word = Word(
                    start=math.floor(raw_word.start * 1000),
                    end=math.floor(raw_word.end * 1000),
                    text=raw_word.word,
                    score=raw_word.probability,
                    is_first=idx == 0,
                    is_last=idx == len(raw_words) - 1,
                )
                words.append(word)
            seg_start = math.floor(raw_seg.start * 1000)
            seg_end = math.floor(raw_seg.end * 1000)
            seg = Segment(start=seg_start, end=seg_end, text=raw_seg.text, words=words)
            segments.append(seg)
        return segments


class SttModelWhisperX(SttModel):
    def __init__(self, model_size: str, compute_type: str, batch_size: int):
        self.__model_size = model_size
        self.__compute_type = compute_type
        self.__batch_size = batch_size

    def transcribe(self, audio_file_path: str, language: str) -> list[Segment]:
        model = whisperx.load_model(self.__model_size, CUDA_DEVICE, compute_type=self.__compute_type)
        log.info("Load model")
        audio = whisperx.load_audio(audio_file_path)
        result = model.transcribe(audio, language=language, batch_size=self.__batch_size)

        gc.collect()
        torch.cuda.empty_cache()
        del model

        model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=CUDA_DEVICE)
        result = whisperx.align(result["segments"], model_a, metadata, audio, CUDA_DEVICE, return_char_alignments=False)
        segments = []
        for raw_seg in result["segments"]:
            raw_words = raw_seg["words"]
            words = []
            for idx, raw_word in enumerate(raw_words):
                word = Word(
                    start=math.floor(raw_word["start"] * 1000),
                    end=math.floor(raw_word["end"] * 1000),
                    text=raw_word["word"],
                    score=raw_word["score"],
                    is_first=idx == 0,
                    is_last=idx == len(raw_words) - 1,
                )
                words.append(word)
            seg_start = math.floor(raw_seg["start"] * 1000)
            seg_end = math.floor(raw_seg["end"] * 1000)
            seg = Segment(start=seg_start, end=seg_end, text=raw_seg["text"], words=words)
            segments.append(seg)

        gc.collect()
        torch.cuda.empty_cache()
        del model_a

        return segments
