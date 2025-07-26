import gc
import math

import torch
import whisperx
from pyutils import log

from sttt.common import Word, Segment

CUDA_DEVICE = "cuda"


class SttModel:
    def __init__(self, model_size: str, compute_type: str, batch_size: int):
        self.__model_size = model_size
        self.__compute_type = compute_type
        self.__batch_size = batch_size

    def transcribe(self, audio_file_path: str) -> list[Segment]:
        model = whisperx.load_model(self.__model_size, CUDA_DEVICE, compute_type=self.__compute_type)
        log.info("Load model")
        audio = whisperx.load_audio(audio_file_path)
        result = model.transcribe(audio, batch_size=self.__batch_size)

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
            seg = Segment(
                start=math.floor(raw_seg["start"] * 1000),
                end=math.floor(raw_seg["end"] * 1000),
                text=raw_seg["text"],
                words=words,
            )
            segments.append(seg)

        gc.collect()
        torch.cuda.empty_cache()
        del model_a

        return segments
