import os

from pydantic import BaseModel

default_env = "dev"
default_model_compute_type = "int8"
default_model_batch_size = "8"
default_word_gap_threshold_ms = "600"
default_phones_per_ms = "100"
default_source_language = "en"


class Env(BaseModel):
    py_env: str
    model_size: str
    model_compute_type: str
    model_batch_size: int

    seg_relocation: bool
    word_gap_threshold_ms: int
    phones_check: bool
    phones_per_ms: int

    source_language: str

    src_path: str
    dst_path: str
    tsvc_base_url: str
    ts_batch_size: int
    ts_first: bool


def get_env() -> Env:
    return Env(
        py_env=os.getenv("PY_ENV") or default_env,
        model_size=os.getenv("MODEL_SIZE") or None,  # type: ignore
        model_compute_type=os.getenv("MODEL_COMPUTE_TYPE", default_model_compute_type),
        model_batch_size=os.getenv("MODEL_BATCH_SIZE", default_model_batch_size),  # type: ignore
        seg_relocation=os.getenv("SEG_RELOCATION") == "true",
        word_gap_threshold_ms=os.getenv("WORD_GAP_THRESHOLD_MS", default_word_gap_threshold_ms),  # type: ignore
        phones_check=os.getenv("PHONES_CHECK") == "true",
        phones_per_ms=os.getenv("PHONES_PER_MS", default_phones_per_ms),  # type: ignore
        source_language=os.getenv("SOURCE_LANGUAGE", default_source_language),
        src_path=os.getenv("APP_SRC_PATH") or None,  # type: ignore
        dst_path=os.getenv("APP_DST_PATH") or None,  # type: ignore
        tsvc_base_url=os.getenv("TSVC_BASE_URL") or None,  # type: ignore
        ts_batch_size=os.getenv("TS_BATCH_SIZE"),  # type: ignore
        ts_first=os.getenv("TS_FIRST") == "true",
    )
