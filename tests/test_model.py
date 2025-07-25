import time
from unittest import TestCase

from sttt.model import SttModel
from sttt.phones import set_espeak_path
from sttt.transcriber import Transcriber
from sttt.vtt import to_vtt_string

set_espeak_path()


# pytest not working due to tqdm conflict
class MyTests(TestCase):
    def test_model(self):
        print()
        start = time.time()

        model_size = "turbo"
        # model_size = "large-v3"
        compute_type = "int8"
        # compute_type = "float16"
        term_time_ms = 500
        # term_time_ms = 700
        relocation = True
        # relocation = False
        per_char_ms = 50
        model = SttModel(
            model_size=model_size,
            compute_type=compute_type,
        )
        transcriber = Transcriber(
            model=model,
            term_time_ms=term_time_ms,
            per_phone_ms=per_char_ms,
            relocation=relocation,
        )
        print(f"{time.time() - start:.4f} sec")

        start = time.time()
        file_path = "../dev/test/assets/out.aac"
        sentences = transcriber.transcribe(file_path)
        print(f"{time.time() - start:.4f} sec")

        vtt = to_vtt_string(sentences)
        print(vtt)
