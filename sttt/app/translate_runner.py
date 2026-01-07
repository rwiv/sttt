import json
import os
import sys

from pyutils import log, stem, path_join, read_file, write_file

from .env import get_env, Env
from ..common import Sentence, Segment
from ..trans import Transcriber, Translator, create_model
from ..utils import to_webvtt_string, set_espeak_path


def run_translate():
    env = get_env()
    log.info("Environment loaded", env.model_dump(mode="json"))

    if sys.platform.startswith("win"):
        set_espeak_path()

    _, source_lang, dest_lang = resolve_lang(env)

    model = create_model(
        model_type=env.model_type,
        model_size=env.model_size,
        compute_type=env.model_compute_type,
        batch_size=env.model_batch_size,
    )
    transcriber = Transcriber(
        silence_threshold_ms=env.silence_threshold_ms,
        seg_relocation=env.seg_relocation,
        word_threshold=env.word_threshold,
        phones_check=env.phones_check,
        phones_per_ms=env.phones_per_ms,
    )
    translator = Translator(
        tsvc_base_url=env.tsvc_base_url,
        batch_size=env.ts_batch_size,
        ts_first=env.ts_first,
        dest_lang=dest_lang,
    )

    os.makedirs(env.dst_path, exist_ok=True)
    for filename in os.listdir(env.src_path):
        src_file_path = path_join(env.src_path, filename)
        out_filename = filename

        if filename.endswith("_sent.json"):
            out_filename = filename.replace("_sent.json", ".json")
            sentences: list[Sentence] = []
            for data in json.loads(read_file(src_file_path)):
                sentences.append(Sentence(**data))
        elif filename.endswith("_seg.json"):
            out_filename = filename.replace("_seg.json", ".json")
            segments: list[Segment] = []
            for data in json.loads(read_file(src_file_path)):
                segments.append(Segment(**data))
            sentences = transcriber.transcribe(segments)
            write_file(
                path_join(env.dst_path, f"{stem(out_filename)}._sent.json"),
                json.dumps([s.model_dump(mode="json") for s in sentences], indent=2, ensure_ascii=False),
            )
        else:
            segments = model.transcribe(audio_file_path=src_file_path, language=source_lang)
            log.info(f"Transcribed audio: {filename}")
            write_file(
                path_join(env.dst_path, f"{stem(filename)}_seg.json"),
                json.dumps([s.model_dump(mode="json") for s in segments], indent=2, ensure_ascii=False),
            )
            sentences = transcriber.transcribe(segments)
            write_file(
                path_join(env.dst_path, f"{stem(filename)}_sent.json"),
                json.dumps([s.model_dump(mode="json") for s in sentences], indent=2, ensure_ascii=False),
            )

        write_file(path_join(env.dst_path, f"{stem(out_filename)}_src.vtt"), to_webvtt_string(sentences))
        translated, merged = translator.translate(sentences)
        write_file(path_join(env.dst_path, f"{stem(out_filename)}_ts.vtt"), to_webvtt_string(translated))
        write_file(path_join(env.dst_path, f"{stem(out_filename)}_merge.vtt"), to_webvtt_string(merged))

        log.info(f"Complete {filename}")


def resolve_lang(env: Env):
    if env.source_language == "en":
        espeak_lang = "en-us"
    elif env.source_language == "ko":
        espeak_lang = "ko"
    else:
        raise ValueError("Invalid source language")

    if env.source_language == "en":
        source_lang = "en"
    elif env.source_language == "ko":
        source_lang = "ko"
    else:
        raise ValueError("Invalid source language")

    if env.source_language == "en":
        dest_lang = "ko"
    elif env.source_language == "ko":
        dest_lang = "en"
    else:
        raise ValueError("Invalid source language")

    return espeak_lang, source_lang, dest_lang
