"""
This is a main module of the app. Contains all api endpoints with minimal business logic
"""

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.src.data_loader import DataLoader
from app.src.options import UnderLayingAsset, Options, OptionPriceCalculationData

app = FastAPI(title="FastAPI for option Pricing")


@app.get("/", response_class=RedirectResponse)
def read_root():
    """
    Landing Page, redirected to document page
    :return: 127.0.0.1/docs
    """
    return RedirectResponse("/docs")


@app.get("/save-market-data",
         description="End point to get last one year data data for underlying asset and save it as csv")
def save_market_data(ticker: str):
    """
    This end point saved data for proveded ticker into data folder
    :param ticker: 'AAPL', 'GOOG', 'SPY' etc.
    :return: Save csv file in data folder
    """
    data_loader = DataLoader(underlaying_ticker=ticker)
    data_loader.save_historical_asset_data()
    return f"Underlying asset data for last one year has been saved at {data_loader.datafile_path}"


@app.get("/show-market-data",
         description="End point to get last one year data data for underlying asset and save it as csv")
def show_market_data(ticker: str):
    """
    This endpoint display data for given ticker from data folder
    :param ticker: 'AAPL', 'GOOG', 'SPY' etc.
    :return:
    """
    data_loader = DataLoader(underlaying_ticker=ticker)
    return data_loader.historical_asset_data()[1]


@app.get("/option-price", description="End point to calculate option price")
def get_option_price(ticker: str, expiry_date: str, strike_price: float, option_type: str = 'call'):
    """
    This endpoint calculates option price for given underlying assert for expiry date and strike price provided
    :param ticker: 'AAPL', 'GOOG', 'SPY' etc.
    :param expiry_date: "%m-%d-%Y" format e.g. 12-18-2023
    :param strike_price: 570.23
    :param option_type: 'call' or 'put'
    :return: options details with input parameter and output price
    """
    underlaying_asset = UnderLayingAsset(ticker=ticker)
    price_calc_data = OptionPriceCalculationData(underlaying_asset)
    options = Options(price_calc_data=price_calc_data, expiry_date=expiry_date, strike_price=strike_price,
                      type=option_type)
    return options.details
