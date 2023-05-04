import os
from dataclasses import dataclass
from datetime import timedelta
from datetime import datetime, date

import pandas as pd
import pandas_datareader.data as pdr

import yfinance as yf

yf.pdr_override()


@dataclass
class DataLoader:
    underlaying_ticker: str = 'SPY'
    today: datetime = datetime.now()
    yesterday: datetime = today - timedelta(days=1)
    date_year_ago: datetime = today - timedelta(days=365)

    def datafolder(self):
        os.makedirs('data', exist_ok=True)

    @property
    def datafile_name(self):
        self.datafolder()
        return f"{self.underlaying_ticker.lower()}_{str(self.today.date())}_data.csv"

    @property
    def datafile_path(self):
        return f"data/{self.datafile_name}"

    @property
    def raw_datafile_path(self):
        return f"data/raw_{self.datafile_name}"

    def last_one_year_raw_data(self):
        raw_data = pdr.get_data_yahoo(self.underlaying_ticker, self.date_year_ago, self.today)
        self.save_data(data=raw_data, filepath=self.raw_datafile_path)

    def save_historical_asset_data(self):
        if not os.path.exists(self.raw_datafile_path):
            self.last_one_year_raw_data()
        if not os.path.exists(self.datafile_path):
            raw_data = pd.read_csv(self.raw_datafile_path)
            df = raw_data.sort_values(by="Date")
            df = df.dropna()
            df = df.assign(close_day_before=df.Close.shift(1))
            df['returns'] = ((df.Close - df.close_day_before) / df.close_day_before)
            self.save_data(data=df, filepath=self.datafile_path)

    @property
    def risk_free_interest_rate(self) -> float:
        """
        This will return avg. of last 10 years return from Tresury
        :return: intrest free return r
        """
        return (pdr.get_data_yahoo(
            "^TNX", self.yesterday, self.today)['Close'].iloc[-1]) / 100

    @staticmethod
    def save_data(data: pd.DataFrame, filepath: str):
        data.to_csv(filepath)

    def historical_asset_data(self) -> dict:
        if not os.path.exists(self.datafile_path):
            self.save_historical_asset_data()
        df = pd.read_csv(self.datafile_path)
        df_to_display = df.dropna().to_dict(orient="index")
        return df, df_to_display
