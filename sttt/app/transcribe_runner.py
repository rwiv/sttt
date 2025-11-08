import os

import yt_dlp
from pyutils import log, stem, path_join, write_file

from .env import get_env
from ..common import Sentence
from ..trans import create_model


def run_transcribe():
    env = get_env()
    log.info("Environment loaded", env.model_dump(mode="json"))

    # Get video urls
    url_file_path = env.urls_file_path
    if url_file_path is None:
        raise ValueError("urls_file_path is None")
    urls = []
    with open(url_file_path, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f.readlines() if line.strip() != ""]

    # Download and extract audio files
    ydl_opts = {
        "format": "bestaudio/best",
        "paths": {"home": env.src_path},
        # 'outtmpl': '%(title)s.%(ext)s',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(urls)

    # Load model
    model = create_model(
        model_type=env.model_type,
        model_size=env.model_size,
        compute_type=env.model_compute_type,
        batch_size=env.model_batch_size,
    )

    # Transcribe audio files
    os.makedirs(env.dst_path, exist_ok=True)
    for filename in os.listdir(env.src_path):
        src_file_path = path_join(env.src_path, filename)
        out_filename = filename

        segments = model.transcribe(audio_file_path=src_file_path, language=env.source_language)
        sentences = [Sentence(start=s.start, end=s.end, text=s.text.strip()) for s in segments]

        text = ""
        for s in sentences:
            text += f"{s.text}\n\n"
        write_file(path_join(env.dst_path, f"{stem(out_filename)}.txt"), text)
        os.remove(src_file_path)

        log.info(f"Complete {filename}")
