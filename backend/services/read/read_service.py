import pandas as pd
from pandas import DataFrame


class ReadService:
    @staticmethod
    def read_csv(path: str) -> DataFrame:
        return pd.read_csv(path)


