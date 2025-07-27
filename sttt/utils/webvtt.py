from ..common import Sentence


def to_webvtt_string(sentences: list[Sentence]):
    vtt_str = "WEBVTT\n\n"
    for chunk in sentences:
        vtt_str += f"{_to_webvtt_block(chunk)}\n"
    return vtt_str


def _to_webvtt_block(seg: Sentence) -> str:
    result = f"{_to_webvtt_timestamp(seg.start)} --> {_to_webvtt_timestamp(seg.end)}\n"
    result += f"{seg.text}\n"
    return result


def _to_webvtt_timestamp(ms: int):
    ph = 3600000  # milliseconds in an hour
    pm = 60000  # milliseconds in a minute
    ps = 1000  # milliseconds in a second

    rest = ms

    hour = rest // ph
    rest %= ph

    minute = rest // pm
    rest %= pm

    sec = rest / ps

    chunks = f"{sec:.3f}".split(".")
    left = chunks[0].zfill(2)
    right = chunks[1].ljust(3, "0")[:3]  # Ensure 3 digits in milliseconds

    hour_string = str(hour).zfill(2)
    minute_string = str(minute).zfill(2)

    return f"{hour_string}:{minute_string}:{left}.{right}"
