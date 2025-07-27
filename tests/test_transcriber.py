import time
from unittest import TestCase

from phonemizer.backend import EspeakBackend
from pyutils import load_dotenv, path_join, find_project_root

from sttt.app import get_env
from sttt.trans import SttModel, Transcriber
from sttt.utils import to_vtt_string, set_espeak_path

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
        per_phone_ms = 100
        relocation = True
        # relocation = False

        model = SttModel(
            model_size=model_size,
            compute_type=compute_type,
            batch_size=batch_size,
        )
        transcriber = Transcriber(
            phone_backend=EspeakBackend("en-us"),
            word_gap_threshold_ms=gap_threshold_ms,
            per_phone_ms=per_phone_ms,
            relocation=relocation,
            check_phones=True,
        )
        print(f"{time.time() - start:.4f} sec")

        start = time.time()
        file_path = "../dev/test/assets/out.aac"
        segments = model.transcribe(audio_file_path=file_path, language="en")
        sentences = transcriber.transcribe(segments)
        print(f"{time.time() - start:.4f} sec")

        vtt = to_vtt_string(sentences)
        print(vtt)
