import os

from lec02.hw.job1.dal.local_disk import save_to_disk
from lec02.hw.job1.dal.sales_api import get_sales
from lec02.hw.utils.file_utils import clear_directory


def save_sales_to_local_disk(date: str, raw_dir: str) -> None:
    clear_directory(raw_dir)

    file_path = os.path.join(raw_dir, f"sales_{date}.json")

    data_written = save_to_disk(get_sales(date), file_path)

    if not data_written and os.path.exists(file_path):
        os.remove(file_path)
        print(f"No sales data saved for {date}. File not created.")
    elif data_written:
        print(f"Sales data saved to {file_path}")
