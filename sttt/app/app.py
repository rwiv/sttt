import json
import os
import sys

from phonemizer.backend import EspeakBackend
from pyutils import log, stem, path_join, read_file, write_file

from .env import get_env
from ..common import Sentence
from ..trans import SttModel, Transcriber, Translator
from ..utils import to_vtt_string, set_espeak_path


def run():
    env = get_env()
    log.info("Environment loaded", env.model_dump(mode="json"))

    if sys.platform.startswith("win"):
        set_espeak_path()

    model = SttModel(
        model_size=env.model_size,
        compute_type=env.compute_type,
    )
    transcriber = Transcriber(
        model=model,
        phone_backend=EspeakBackend("en-us"),
        term_time_ms=env.term_time_ms,
        per_phone_ms=env.per_phone_ms,
        relocation=env.relocation,
    )
    translator = Translator(
        tsvc_base_url=env.tsvc_base_url,
        batch_size=env.ts_batch_size,
        ts_first=env.ts_first,
    )

    os.makedirs(env.dst_path, exist_ok=True)
    for filename in os.listdir(env.src_path):
        src_file_path = path_join(env.src_path, filename)

        if filename.endswith(".json"):
            read_file(src_file_path)
            sentences: list[Sentence] = []
            for data in json.loads(read_file(src_file_path)):
                sentences.append(Sentence(**data))
        else:
            sentences = transcriber.transcribe(src_file_path)
            log.info("Transcribed sentences")
            write_file(
                path_join(env.dst_path, f"{stem(filename)}.json"),
                json.dumps([s.model_dump(mode="json") for s in sentences], indent=2),
            )

        write_file(path_join(env.dst_path, f"{stem(filename)}_src.vtt"), to_vtt_string(sentences))
        translated, merged = translator.translate(sentences)
        write_file(path_join(env.dst_path, f"{stem(filename)}_ts.vtt"), to_vtt_string(translated))
        write_file(path_join(env.dst_path, f"{stem(filename)}_merge.vtt"), to_vtt_string(merged))

        log.info(f"Complete {filename}")
