import json
from pathlib import Path
from typing import Any, Dict


class JSONReaderError(Exception):
    pass


def load_json(file_path: str | Path) -> Dict[str, Any]:
    path = Path(file_path)

    if not path.exists():
        raise JSONReaderError(f"File not found: {path}")

    if path.suffix != ".json":
        raise JSONReaderError(f"Invalid file type (expected .json): {path}")

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise JSONReaderError(f"Invalid JSON format: {e}")

    _validate_base_structure(data)

    return data


def _validate_base_structure(data: Dict[str, Any]) -> None:
    required_keys = ["specversion", "challengeid", "metadata", "workload"]

    for key in required_keys:
        if key not in data:
            raise JSONReaderError(f"Missing required key: '{key}'")

    if not isinstance(data["metadata"], dict):
        raise JSONReaderError("'metadata' must be an object")

    if not isinstance(data["workload"], dict):
        raise JSONReaderError("'workload' must be an object")
