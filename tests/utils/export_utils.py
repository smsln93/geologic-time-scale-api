import csv
import json
import re
from pathlib import Path
from typing import List, Dict, Tuple, Any


def read_csv_file(file_dir: Path) -> Tuple[List[Dict[str, str]], Path]:
    file = next(file_dir.iterdir())
    with file.open() as f:
        return list(csv.DictReader(f)), file


def read_json_file(file_dir: Path) -> Tuple[List[Dict[str, Any]], Path]:
    file = next(file_dir.iterdir())
    with file.open() as f:
        return json.load(f), file


def is_valid_export_filename(file: Path) -> bool:
    return re.fullmatch(
        r"exported_data_[0-9a-f]{32}",
        file.stem
    ) is not None