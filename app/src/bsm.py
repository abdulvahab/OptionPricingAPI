from dataclasses import dataclass
from math import sqrt, log, exp

from scipy.stats import norm


@dataclass
class BlackScholesModel:
    """
    Black Scholes Model
    The Black Scholes model is considered to be one of the best ways of determining fair prices of options. It requires five variables: the strike price of an option, the current stock price, the time to expiration, the risk-free rate, and the volatility.

    Black Scholes Formula
    C = call option price
    N = CDF of the normal distribution
    S = spot price of an asset
    K = strike price
    r = risk-free interest rate
    T = time to maturity
    σ = volatility of the asset

    Assumptions Made for this Calculator

    It works on European options that can only be exercised at expiration.
    No dividends paid out during the option’s life.
    No transaction and commissions costs in buying the option.
    The returns on the underlying are normally distributed.

    """
    S: float
    K: float
    r: float
    T: int
    sigma: float

    @property
    def N(self):
        return norm.cdf

    @property
    def d1(self):
        return (log(self.S / self.K) + (self.r + self.sigma ** 2 / 2.) * self.T) / (self.sigma * sqrt(self.T))

    @property
    def d2(self):
        return self.d1 - self.sigma * sqrt(self.T)

    @property
    def bs_call(self, ):
        return self.S * self.N(self.d1) - self.K * exp(-self.r * self.T) * self.N(self.d2)

    @property
    def bs_put(self):
        return self.K * exp(-self.r * self.T) - (self.S * self.bs_call)
