from sttt.model import Sentence


def to_srt_chunk_string(seg: Sentence, num: int) -> str:
    result = f"{num}\n"
    result += f"{to_vtt_time_string(seg.start)} --> {to_vtt_time_string(seg.end)}\n"
    result += f"{seg.text}\n"
    return result


def to_srt_string(chunks: list[Sentence]):
    srt_str = ""
    for idx, chunk in enumerate(chunks):
        srt_str += f"{to_srt_chunk_string(chunk, idx + 1)}\n"
    return srt_str


def to_vtt_string(chunks: list[Sentence]):
    return "WEBVTT\n\n" + to_srt_string(chunks)


def to_vtt_time_string(ms: int):
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

    return f"{hour_string}:{minute_string}:{left},{right}"
