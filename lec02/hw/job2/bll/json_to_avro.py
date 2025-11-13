import json
import os
from typing import List

from lec02.hw.job2.dal.local_disk import read_json_file, save_to_avro_file
from lec02.hw.utils.file_utils import clear_directory

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "..", "sales.avsc")
SCHEMA_PATH = os.path.abspath(SCHEMA_PATH)


def load_avro_schema(schema_path: str) -> dict:
    with open(schema_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json_to_avro(raw_dir: str, stg_dir: str) -> None:
    clear_directory(stg_dir)

    json_files: List[str] = [f for f in os.listdir(raw_dir) if f.endswith(".json")]
    if not json_files:
        print(f"No JSON files found in {raw_dir}")
        return

    for json_file in json_files:
        json_path = os.path.join(raw_dir, json_file)
        data = read_json_file(json_path)
        if not data:
            print(f"No data in {json_path}, skipping.")
            continue

        schema: dict = load_avro_schema(SCHEMA_PATH)

        avro_file_name = json_file.replace(".json", ".avro")
        avro_path = os.path.join(stg_dir, avro_file_name)

        save_to_avro_file(data, schema, avro_path)

        print(f"Saved {avro_path}")