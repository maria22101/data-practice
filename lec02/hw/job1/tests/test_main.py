"""
Tests for main.py
"""
from unittest import TestCase, mock

from lec02.hw.job1 import main


class MainFunctionTestCase(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        main.app.testing = True
        cls.client = main.app.test_client()

    @mock.patch('lec02.hw.job1.main.save_sales_to_local_disk')
    def test_return_400_date_param_missed(self, save_sales_to_local_disk_mock: mock.MagicMock):
        """
        Raise 400 HTTP code when no 'date' param
        """
        resp = self.client.post(
            '/',
            json={
                'raw_dir': '/foo/bar/',
                # no 'date' set!
            },
        )

        self.assertEqual(400, resp.status_code)
        self.assertIn("date parameter missed", resp.get_json()["message"])
        save_sales_to_local_disk_mock.assert_not_called()

    @mock.patch('lec02.hw.job1.main.save_sales_to_local_disk')
    def test_return_400_raw_dir_param_missed(self, save_sales_to_local_disk_mock: mock.MagicMock):
        """
        Raise 400 HTTP code when no 'raw_dir' param
        """
        resp = self.client.post(
            '/',
            json={
                'date': '2022-08-09',
                # no 'raw_dir' set!
            },
        )
        self.assertEqual(400, resp.status_code)
        self.assertIn("raw_dir parameter missed", resp.get_json()["message"])
        save_sales_to_local_disk_mock.assert_not_called()

    @mock.patch('lec02.hw.job1.main.save_sales_to_local_disk')
    def test_save_sales_to_local_disk(self, save_sales_to_local_disk_mock: mock.MagicMock):
        """
        Test whether api.get_sales is called with proper params
        """
        fake_date = '1970-01-01'
        fake_raw_dir = '/foo/bar/'
        self.client.post(
            '/',
            json={
                'date': fake_date,
                'raw_dir': fake_raw_dir,
            },
        )

        save_sales_to_local_disk_mock.assert_called_with(
            date=fake_date,
            raw_dir=fake_raw_dir,
        )

    @mock.patch('lec02.hw.job1.main.save_sales_to_local_disk')
    def test_return_201_when_all_is_ok(self, save_sales_to_local_disk_mock: mock.MagicMock):
        """
        Test that 201 is returned when all params are ok
        """
        fake_date = '2022-08-09'
        fake_raw_dir = '/foo/bar/'
        resp = self.client.post(
            '/',
            json={
                'date': fake_date,
                'raw_dir': fake_raw_dir,
            },
        )
        self.assertEqual(201, resp.status_code)
        self.assertIn("Data retrieved successfully from API", resp.get_json()["message"])
        save_sales_to_local_disk_mock.assert_called_once()
