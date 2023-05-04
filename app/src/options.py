"""
This module contains entities and classes related to options. Sych as underlying asset, calculation parameters,
and Options contract details
"""
from datetime import datetime
from dataclasses import dataclass

import numpy as np


from app.src.bsm import BlackScholesModel
from app.src.data_loader import DataLoader
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class UnderLayingAsset:
    ticker: str

    @property
    def data_loader(self):
        return DataLoader(underlaying_ticker=self.ticker)

    @property
    def historical_data(self):
        return self.data_loader.historical_asset_data()[0]

    @property
    def spot_price_of_asset(self):
        """
        This is spot price for underlying asset
        :return: spot price for options underlaying asset(S)
        """

        return self.historical_data['Close'].iloc[-1]

    @property
    def details(self):
        object_dict = self.to_dict()
        object_dict['spot_price_of_asset'] = self.spot_price_of_asset

        return object_dict


@dataclass_json
@dataclass
class OptionPriceCalculationData:
    underlaying_asset: UnderLayingAsset

    @property
    def hist_data(self):
        return self.underlaying_asset.historical_data

    @property
    def risk_free_interest_rate(self):
        return self.underlaying_asset.data_loader.risk_free_interest_rate

    @property
    def sigma(self):
        return np.sqrt(252) * self.hist_data['returns'].std()


    @property
    def details(self):
        object_dict = self.to_dict()
        object_dict['underlaying_asset'] = self.underlaying_asset.details
        object_dict['sigma'] = self.sigma
        object_dict['risk_free_interest_rate'] = self.risk_free_interest_rate

        return object_dict


@dataclass_json
@dataclass
class Options:
    type: str
    expiry_date: datetime
    strike_price: float
    price_calc_data: OptionPriceCalculationData

    @property
    def time_to_expiry(self) -> float:
        """
        This is time to expiry of option in year
        :return: time to expiry in year (T)
        """

        return (datetime.strptime(self.expiry_date, "%m-%d-%Y") - datetime.utcnow()).days / 365

    @property
    def price(self):
        bsm = BlackScholesModel(
            S=self.price_calc_data.underlaying_asset.spot_price_of_asset,
            K=self.strike_price,
            r=self.price_calc_data.risk_free_interest_rate,
            T=self.time_to_expiry,
            sigma=self.price_calc_data.sigma
        )
        return bsm.bs_call if self.type == 'call' else bsm.bs_put

    @property
    def details(self):
        option_dict = self.to_dict()
        option_dict['time_to_expiry'] = self.time_to_expiry
        option_dict['price'] = self.price
        option_dict['price_calc_data'] = self.price_calc_data.details
        return option_dict
