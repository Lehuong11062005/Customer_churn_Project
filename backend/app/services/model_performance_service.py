import json
from pathlib import Path

MODEL_DIR = (
    Path(__file__).resolve()
    .parent.parent.parent
    / "ml_models"
)

PERFORMANCE_PATH = MODEL_DIR / "model_performance.json"


def get_model_performance():
    if not PERFORMANCE_PATH.exists():
        raise FileNotFoundError(
            f"Không tìm thấy file {PERFORMANCE_PATH}"
        )

    with open(PERFORMANCE_PATH, "r", encoding="utf-8") as file:
        return json.load(file)