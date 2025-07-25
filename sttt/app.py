import json
import os.path

from pyutils import log

from .env import get_env
from .model import SttModel
from .schema import Sentence
from .transcriber import Transcriber
from .vtt import to_vtt_string


def run():
    env = get_env()
    log.info("Environment loaded", env.model_dump(mode="json"))

    model = SttModel(
        model_size=env.model_size,
        compute_type=env.compute_type,
    )
    transcriber = Transcriber(
        model=model,
        term_time_ms=env.term_time_ms,
        per_phone_ms=env.per_phone_ms,
        relocation=env.relocation,
    )

    os.makedirs(env.dst_path, exist_ok=True)
    for filename in os.listdir(env.src_path):
        src_file_path = os.path.join(env.src_path, filename)
        out_file_path = os.path.join(env.dst_path, f"{os.path.splitext(filename)[0]}.vtt")

        if filename.endswith(".json"):
            with open(src_file_path, "r") as f:
                sentences: list[Sentence] = []
                for data in json.loads(f.read()):
                    sentences.append(Sentence(**data))
        else:
            sentences = transcriber.transcribe(src_file_path)
            with open(out_file_path, "w") as f:
                f.write(json.dumps([s.model_dump(mode="json") for s in sentences], indent=2))

        vtt = to_vtt_string(sentences)
        with open(out_file_path, "w") as f:
            f.write(vtt)

        log.info(f"Generated {out_file_path}")
