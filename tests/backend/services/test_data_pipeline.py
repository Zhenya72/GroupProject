import unittest
import pandas as pd
from pandas.testing import assert_frame_equal
from unittest.mock import patch
from backend.services.data_pipeline import DataPipeline


class TestDataPipeline(unittest.TestCase):

    @classmethod
    @patch('backend.services.read.read_service.ReadService.read_csv', side_effect=lambda x: pd.DataFrame({'dummy': [1, 2, 3]}))
    def setUpClass(cls, mock_read_csv):
        cls.data_pipeline = DataPipeline()

    def test_convert_columns_weather_df(self):
        # Test the conversion of columns in the weather DataFrame
        columns_to_exclude = ['date', 'codesum']
        expected_df = pd.DataFrame({'dummy': [1, 2, 3]})

        result_df = self.data_pipeline.convert_columns_weather_df()

        assert_frame_equal(result_df, expected_df)

    def test_convert_columns_dfs_to_datetime(self):
        # Test the conversion of columns to datetime in multiple DataFrames
        expected_df_list = [pd.DataFrame({'dummy': [1, 2, 3}])] * 3

        result_df_list = self.data_pipeline.convert_columns_dfs_to_datetime(pd.DataFrame({'dummy': [1, 2, 3]}))

        for result_df, expected_df in zip(result_df_list, expected_df_list):
            assert_frame_equal(result_df, expected_df)

    def test_merge_dfs_for_server(self):
        # Test the merging of DataFrames in the data pipeline
        expected_train_weather = pd.DataFrame({'dummy': [1, 2, 3]})
        expected_test_weather = pd.DataFrame({'dummy': [1, 2, 3]})
        expected_train_merged = pd.DataFrame({'dummy': [1, 2, 3]})
        expected_test_merged = pd.DataFrame({'dummy': [1, 2, 3]})

        result_train_weather, result_test_weather, result_train_merged, result_test_merged = self.data_pipeline.merge_dfs_for_server()

        assert_frame_equal(result_train_weather, expected_train_weather)
        assert_frame_equal(result_test_weather, expected_test_weather)
        assert_frame_equal(result_train_merged, expected_train_merged)
        assert_frame_equal(result_test_merged, expected_test_merged)


if __name__ == '__main__':
    unittest.main()
