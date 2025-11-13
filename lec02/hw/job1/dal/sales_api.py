import os
from typing import List, Dict, Any, Iterator

import requests

API_URL = 'https://fake-api-vycpfa6oca-uc.a.run.app/sales'


def get_sales(date: str) -> Iterator[List[Dict[str, Any]]]:
    """
    Get data from sales API for specified date.

    :param date: data retrieve the data from
    :return: list of records
    """
    auth_token = os.environ.get("API_AUTH_TOKEN")
    if not auth_token:
        raise ValueError("API_AUTH_TOKEN environment variable must be set")

    page = 1

    while True:
        params = {
            "date": date,
            "page": page
        }
        headers = {
            "Authorization": auth_token
        }
        response = requests.get(API_URL, params=params, headers=headers)
        if response.status_code != 200:
            raise Exception(f"API request failed: url {API_URL} with {response.status_code} {response.text}")

        records = response.json()
        if not records:
            break

        yield records

        if len(records) < 100:
            # no more pages
            break
        page += 1
