import unittest
import pandas as pd
from pandas.testing import assert_frame_equal
from unittest.mock import patch

from backend.services.read.read_service import ReadService


class TestReadService(unittest.TestCase):

    @patch('pandas.read_csv')
    def test_read_csv(self, mock_read_csv):
        # Mock the pandas.read_csv function
        input_path = 'fake_path.csv'
        expected_data = {'ID': [1, 2, 3], 'Name': ['Alice', 'Bob', 'Charlie']}
        expected_df = pd.DataFrame(expected_data)

        mock_read_csv.return_value = expected_df

        result_df = ReadService.read_csv(input_path)

        mock_read_csv.assert_called_once_with(input_path)
        assert_frame_equal(result_df, expected_df)


if __name__ == '__main__':
    unittest.main()
