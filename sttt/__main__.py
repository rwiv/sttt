import sys

from .app import run
from .phones import set_espeak_path

if __name__ == "__main__":
    if sys.platform.startswith("win"):
        set_espeak_path()
    run()
