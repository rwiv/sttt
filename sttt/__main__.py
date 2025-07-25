import sys

from sttt import job
from sttt.phones import set_espeak_path

if __name__ == "__main__":
    if sys.platform.startswith("win"):
        set_espeak_path()
    job.run()
