import json
from typing import List, Dict, Any

from fastavro import writer


def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_to_avro_file(data: List[Dict[str, Any]], schema: Dict[str, Any], path: str) -> None:
    with open(path, "wb") as out:
        writer(out, schema, data)