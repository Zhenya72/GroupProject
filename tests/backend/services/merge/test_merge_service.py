import unittest
import pandas as pd
from pandas.testing import assert_frame_equal

from backend.services.merge.merge_dataframe_service import MergeDFService


class TestMergeDFService(unittest.TestCase):

    def setUp(self):
        # Initialize DataFrames for testing
        data_1 = {'ID': [1, 2, 3], 'Name': ['Alice', 'Bob', 'Charlie']}
        data_2 = {'ID': [2, 3, 4], 'Age': [25, 30, 22]}
        self.df_1 = pd.DataFrame(data_1)
        self.df_2 = pd.DataFrame(data_2)

    def test_merge(self):
        # Test merging DataFrames based on specified columns
        columns_key = ['ID']
        expected_data = {'ID': [2, 3], 'Name': ['Bob', 'Charlie'], 'Age': [25, 30]}
        expected_df = pd.DataFrame(expected_data)

        result_df = MergeDFService.merge(self.df_1, self.df_2, columns_key)

        assert_frame_equal(result_df, expected_df)

    def test_merge_invalid_column(self):
        # Test merging with an invalid key column
        invalid_columns_key = ['InvalidColumn']
        with self.assertRaises(KeyError):
            MergeDFService.merge(self.df_1, self.df_2, invalid_columns_key)


if __name__ == '__main__':
    unittest.main()
