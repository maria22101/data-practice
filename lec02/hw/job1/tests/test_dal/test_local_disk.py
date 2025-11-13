"""
Tests dal.local_disk.py module
"""
import json
import os
import shutil
import tempfile
from unittest import TestCase

from lec02.hw.job1.dal.local_disk import save_to_disk


class SaveToDiskTestCase(TestCase):
    """
    Test dal.local_disk.save_to_disk function.
    """
    def setUp(self):
        # create temporary directory for test
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, "test.json")

    def tearDown(self):
        # delete the temporary directory after test run
        shutil.rmtree(self.test_dir)

    def test_save_to_disk_with_data(self):
        # test data - 2 pages:
        page_iterator = [
            [{"a": 1, "b": "x"}],
            [{"a": 2, "b": "y"}]
        ]
        result = save_to_disk(page_iterator, self.test_file)

        # Asserts
        # method's return value:
        self.assertTrue(result)

        # file created:
        self.assertTrue(os.path.exists(self.test_file))

        # file content:
        with open(self.test_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data, [{"a": 1, "b": "x"}, {"a": 2, "b": "y"}])

    def test_save_to_disk_no_data(self):
        # empty test data
        page_iterator = []
        result = save_to_disk(page_iterator, self.test_file)
        self.assertFalse(result)
        self.assertFalse(os.path.exists(self.test_file))
