import json
from typing import Dict, Any, Iterable


def save_to_disk(page_iterator: Iterable[Iterable[Dict[str, Any]]], path: str) -> bool:
    data_written = False
    first = True
    f = None
    try:
        for page_records in page_iterator:
            if not data_written:
                f = open(path, "w", encoding="utf-8")
                f.write("[\n")
                data_written = True
            for record in page_records:
                if not first:
                    f.write(",\n")
                f.write(json.dumps(record, ensure_ascii=False))
                first = False
        if data_written:
            f.write("\n]\n")
            f.close()
    except Exception:
        if data_written and f:
            f.close()
        raise
    return data_written
