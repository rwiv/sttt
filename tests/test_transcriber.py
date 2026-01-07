import time
from unittest import TestCase

from pyutils import load_dotenv, path_join, find_project_root

from sttt.app import get_env
from sttt.trans import create_model, Transcriber
from sttt.utils import to_webvtt_string, set_espeak_path

set_espeak_path()
load_dotenv(path_join(find_project_root(), "dev", ".env"))

env = get_env()


# pytest not working due to tqdm conflict
class MyTests(TestCase):
    def test_model(self):
        print()
        start = time.time()

        model_size = "base"
        # model_size = "turbo"
        # model_size = "large-v3"
        # compute_type = "int8"
        compute_type = "float16"
        # batch_size = 8
        batch_size = 16

        gap_threshold_ms = 600
        phones_per_ms = 100
        seg_relocation = True
        # seg_relocation = False

        model = create_model(
            model_type="whisperx",
            model_size=model_size,
            compute_type=compute_type,
            batch_size=batch_size,
        )
        transcriber = Transcriber(
            silence_threshold_ms=gap_threshold_ms,
            seg_relocation=seg_relocation,
            word_threshold=10,
            phones_check=False,
            phones_per_ms=phones_per_ms,
        )
        print(f"{time.time() - start:.4f} sec")

        start = time.time()
        file_path = "../dev/test/assets/out.aac"
        segments = model.transcribe(audio_file_path=file_path, language="en")
        sentences = transcriber.transcribe(segments)
        print(f"{time.time() - start:.4f} sec")

        vtt = to_webvtt_string(sentences)
        print(vtt)
