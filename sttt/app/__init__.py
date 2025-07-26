import sys

from .app import run
from .env import get_env

targets = [
    "app",
    "env",
]
for name in list(sys.modules.keys()):
    for target in targets:
        if name.startswith(f"{__name__}.{target}"):
            sys.modules[name] = None  # type: ignore
