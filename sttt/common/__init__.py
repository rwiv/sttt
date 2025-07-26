import sys

from .schema import Sentence, Word, Segment

targets = [
    "schema",
]
for name in list(sys.modules.keys()):
    for target in targets:
        if name.startswith(f"{__name__}.{target}"):
            sys.modules[name] = None  # type: ignore
