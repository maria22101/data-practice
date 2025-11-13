"""
Tests dal.sales_api.py module.
"""
from unittest import TestCase, mock

from lec02.hw.job1.dal.sales_api import get_sales


class GetSalesTestCase(TestCase):
    """
    Test dal.sales_api.get_sales function.
    """

    @mock.patch("lec02.hw.job1.dal.sales_api.requests.get")
    def test_get_sales_multiple_pages(self, mock_get):
        # test data (API mocked responses):
        mock_get.side_effect = [
            mock.Mock(status_code=200, json=mock.Mock(return_value=[
                {"client": "A", "price": 100},
                {"client": "B", "price": 200}
            ]))
        ]

        # mock environment variable
        with mock.patch.dict("os.environ", {"API_AUTH_TOKEN": "fake_token"}):
            result = list(get_sales("2022-08-09"))

        # Assert
        self.assertEqual(result, [
            [
                {"client": "A", "price": 100},
                {"client": "B", "price": 200}
            ]
        ])

    @mock.patch("lec02.hw.job1.dal.sales_api.requests.get")
    def test_get_sales_no_data(self, mock_get):
        # test data (API mocked responses):
        mock_get.return_value = mock.Mock(status_code=200, json=mock.Mock(return_value=[]))

        with mock.patch.dict("os.environ", {"API_AUTH_TOKEN": "fake_token"}):
            result = list(get_sales("2022-08-09"))

        self.assertEqual(result, [])

    @mock.patch("lec02.hw.job1.dal.sales_api.requests.get")
    def test_get_sales_raises_on_error(self, mock_get):
        # API call causes 500 error
        mock_get.return_value = mock.Mock(status_code=500, text="Server error")

        with mock.patch.dict("os.environ", {"API_AUTH_TOKEN": "fake_token"}):
            with self.assertRaises(Exception) as context:
                list(get_sales("2022-08-09"))
            self.assertIn("API request failed", str(context.exception))

    def test_get_sales_no_token(self):
        # No environment variable set
        with mock.patch.dict("os.environ", {}, clear=True):
            with self.assertRaises(ValueError) as context:
                list(get_sales("2022-08-09"))
            self.assertIn("API_AUTH_TOKEN environment variable must be set", str(context.exception))
