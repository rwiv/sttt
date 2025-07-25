import os

from pydantic import BaseModel

default_env = "dev"
default_model_size = "base"
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


def get_env() -> Env:
    src_path = os.getenv("APP_SRC_PATH")
    if not src_path:
        raise ValueError("APP_SRC_PATH is required")
    dst_path = os.getenv("APP_DST_PATH")
    if not dst_path:
        raise ValueError("APP_DST_PATH is required")

    return Env(
        py_env=os.getenv("PY_ENV") or default_env,
        model_size=os.getenv("MODEL_SIZE", default_model_size),
        compute_type=os.getenv("MODEL_COMPUTE_TYPE", default_compute_type),
        term_time_ms=int(os.getenv("SEG_TERM_TIME_MS", default_term_time_ms)),
        per_phone_ms=int(os.getenv("SEG_PER_PHONE_MS", default_per_phone_ms)),
        relocation=os.getenv("SEG_RELOCATION", default_relocation).lower() == "true",
        src_path=src_path,
        dst_path=dst_path,
    )
