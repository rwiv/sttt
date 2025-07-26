import os

from pydantic import BaseModel

default_env = "dev"
default_compute_type = "int8"
default_term_time_ms = "500"
default_per_phone_ms = "100"
default_relocation = "true"


class Env(BaseModel):
    py_env: str
    model_size: str
    compute_type: str
    term_time_ms: int
    per_phone_ms: int
    relocation: bool
    src_path: str
    dst_path: str
    tsvc_base_url: str
    ts_batch_size: int
    ts_first: bool


def get_env() -> Env:
    return Env(
        py_env=os.getenv("PY_ENV") or default_env,
        model_size=os.getenv("MODEL_SIZE") or None,  # type: ignore
        compute_type=os.getenv("MODEL_COMPUTE_TYPE", default_compute_type),
        term_time_ms=os.getenv("SEG_TERM_TIME_MS", default_term_time_ms),  # type: ignore
        per_phone_ms=os.getenv("SEG_PER_PHONE_MS", default_per_phone_ms),  # type: ignore
        relocation=os.getenv("SEG_RELOCATION", default_relocation).lower() == "true",
        src_path=os.getenv("APP_SRC_PATH") or None,  # type: ignore
        dst_path=os.getenv("APP_DST_PATH") or None,  # type: ignore
        tsvc_base_url=os.getenv("TSVC_BASE_URL") or None,  # type: ignore
        ts_batch_size=os.getenv("TS_BATCH_SIZE"),  # type: ignore
        ts_first=os.getenv("TS_FIRST") == "true",
    )
