import pandas as pd
from pandas import DataFrame


class MergeDFService:
    @staticmethod
    def merge(df_1: DataFrame, df_2: DataFrame, columns_key: list) -> DataFrame:
        return pd.merge(df_1, df_2, on=columns_key)

