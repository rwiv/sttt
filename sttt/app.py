import os.path

from pyutils import log

from .env import get_env
from .model import SttModel
from .transcriber import Transcriber
from .vtt import to_vtt_string


def run():
    env = get_env()
    log.info("Environment loaded", env.to_dict())

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
        audio_path = os.path.join(env.src_path, filename)
        out_path = os.path.join(env.dst_path, f"{os.path.splitext(filename)[0]}.vtt")

        segments = transcriber.transcribe(audio_path)
        vtt = to_vtt_string(segments)

        with open(out_path, "w") as f:
            f.write(vtt)
        log.info(f"Generated {out_path}")
