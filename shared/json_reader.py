from pathlib import Path
import argparse
import sys

def read_code(file_path: str) -> str:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Path not found: {file_path}")
    if not path.is_file():
        raise IsADirectoryError(f"Expected a file, got: {file_path}")

    return path.read_text(encoding="utf-8")