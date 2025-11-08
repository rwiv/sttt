import sys


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m sttt <transcribe|translate>")
        sys.exit(1)

    mode = sys.argv[1]

    if mode == "transcribe":
        from .app import run_transcribe

        run_transcribe()
    elif mode == "translate":
        from .app import run_translate

        run_translate()
    else:
        print(f"Unknown mode: {mode}")
        sys.exit(1)
