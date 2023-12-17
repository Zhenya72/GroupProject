import pandas as pd
from pandas import DataFrame


class Converter:
    def __init__(self, df: DataFrame):
        self.df = df

    def convert_all_columns_except(self, columns: list):
        for data in self.df:
            if data not in columns:
                self.df[data] = pd.to_numeric(self.df[data], errors='coerce')
        return self.df

    def convert_col_to_datetime(self, column: str):
        self.df[column] = pd.to_datetime(self.df[column])
        return self.df



