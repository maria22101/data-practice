"""
This file contains the controller that accepts command via HTTP
and triggers the business logic layer for job2 (JSON → Avro)
"""
from flask import Flask, request
from flask import typing as flask_typing

from lec02.hw.job2.bll.json_to_avro import save_json_to_avro

app = Flask(__name__)


@app.route('/', methods=['POST'])
def main() -> flask_typing.ResponseReturnValue:
    """
    Controller that accepts command via HTTP and
    triggers business logic layer

    POST body in JSON:
    {
      "raw_dir": "/path/to/my_dir/raw/sales/2022-08-09",
      "stg_dir": "/path/to/my_dir/stg/sales/2022-08-09"
    }
    """
    input_data: dict = request.json
    raw_dir = input_data.get('raw_dir')
    stg_dir = input_data.get('stg_dir')

    if not raw_dir or not stg_dir:
        return {
            "message": "raw_dir and stg_dir parameters are required",
        }, 400

    save_json_to_avro(raw_dir=raw_dir, stg_dir=stg_dir)

    return {
        "message": "Data successfully converted from JSON to Avro"
    }, 201


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=8082)