import sys

from .webvtt import to_vtt_string

targets = [
    "phones",
    "webvtt",
]
for name in list(sys.modules.keys()):
    for target in targets:
        if name.startswith(f"{__name__}.{target}"):
            sys.modules[name] = None  # type: ignore
