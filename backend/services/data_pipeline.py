from backend.services.read.read_service import ReadService
from backend.services.merge.merge_dataframe_service import MergeDFService
from backend.services.convert.convert_service import Converter
from backend.config.config_path import ConfigPath

from pandas import DataFrame


class DataPipeline:
    def __init__(self):
        self._load_dataframes()

    def _load_dataframes(self):
        self.df_key = ReadService.read_csv(ConfigPath.KEY_FILE_PATH)
        self.df_sample_submission = ReadService.read_csv(
            ConfigPath.SAMPLE_SUBMISSION_FILE_PATH)
        self.df_weather = ReadService.read_csv(ConfigPath.WEATHER_FILE_PATH)
        self.df_train = ReadService.read_csv(ConfigPath.TRAIN_FILE_PATH)
        self.df_test = ReadService.read_csv(ConfigPath.TEST_FILE_PATH)

        self._preprocess_data()

    def _preprocess_data(self):
        self.df_train = self.df_train.head(int(0.7 * len(self.df_train)))

    @staticmethod
    def get_sorted_weather_df(columns: list, df_sort_weather: DataFrame):
        return df_sort_weather.loc[:, columns]

    def convert_columns_weather_df(self):
        return Converter(self.df_weather).convert_all_columns_except(['date', 'codesum'])

    def convert_columns_dfs_to_datetime(self, df_weather, column="date"):
        return [Converter(df).convert_col_to_datetime(column)
                for df in [self.df_train, self.df_test, df_weather]]

    def merge_dfs_for_server(self):
        df_weather = self.convert_columns_weather_df()
        df_train, df_test, df_weather = self.convert_columns_dfs_to_datetime(df_weather)
        df_sort_weather = self.get_sorted_weather_df(
            ['station_nbr', 'date', 'codesum', 'preciptotal'],
            df_weather
        )
        train_merged = MergeDFService.merge(df_train, self.df_key, ['store_nbr'])
        test_merged = MergeDFService.merge(df_test, self.df_key, ['store_nbr'])

        train_weather = MergeDFService.merge(train_merged, df_sort_weather, ['station_nbr', 'date'])
        test_weather = MergeDFService.merge(test_merged, df_sort_weather, ['station_nbr', 'date'])

        return train_weather, test_weather, train_merged, test_merged


