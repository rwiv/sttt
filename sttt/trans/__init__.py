import sys

from .model import SttModel, SttModelFasterWhisper, SttModelWhisperX
from .transcriber import Transcriber
from .translator import Translator

targets = [
    "model",
    "schema",
    "transcriber",
    "translator",
]
for name in list(sys.modules.keys()):
    for target in targets:
        if name.startswith(f"{__name__}.{target}"):
            sys.modules[name] = None  # type: ignore
