import unittest
import pandas as pd
from pandas.testing import assert_frame_equal

from backend.services.convert.convert_service import Converter


class TestConverter(unittest.TestCase):

    def setUp(self):
        # Initialize a DataFrame for testing
        data = {'A': ['1', '2', '3'],
                'B': ['4', '5', '6'],
                'C': ['2021-01-01', '2021-02-02', '2021-03-03']}
        self.df = pd.DataFrame(data)
        self.converter = Converter(self.df.copy())

    def test_convert_all_columns_except(self):
        # Test conversion of all columns except specified ones
        columns_to_exclude = ['B']
        expected_df = self.df.copy()
        expected_df['A'] = pd.to_numeric(expected_df['A'], errors='coerce')
        expected_df['C'] = pd.to_numeric(expected_df['C'], errors='coerce')

        result_df = self.converter.convert_all_columns_except(columns_to_exclude)

        assert_frame_equal(result_df, expected_df)

    def test_convert_col_to_datetime(self):
        # Test conversion of a specific column to datetime
        column_to_convert = 'C'
        expected_df = self.df.copy()
        expected_df['C'] = pd.to_datetime(expected_df['C'])

        result_df = self.converter.convert_col_to_datetime(column_to_convert)

        assert_frame_equal(result_df, expected_df)

    def test_convert_col_to_datetime_invalid_column(self):
        # Test conversion of an invalid column to datetime
        invalid_column = 'InvalidColumn'
        with self.assertRaises(KeyError):
            self.converter.convert_col_to_datetime(invalid_column)


if __name__ == '__main__':
    unittest.main()
