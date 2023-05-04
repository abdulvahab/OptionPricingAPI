# Introduction
This repository is for Option Pricing API. The source we use is yahoo finance for pulling data for underlying asset (needed to calculate option price)

The formula which we use to calculate options price is BlackScholesModel. 

## Black Scholes Model
The Black Scholes model is considered to be one of the best ways of determining fair prices of options. It requires five variables: the strike price of an option, the current stock price, the time to expiration, the risk-free rate, and the volatility.
                    
                    ![bsm](https://drive.google.com/file/d/1N1pUaOAzDeCzGfCkyE2pOy2i1_tysSI-/view?usp=share_link)

Black Scholes Formula
C = call option price
N = CDF of the normal distribution
St= spot price of an asset
K = strike price
r = risk-free interest rate
t = time to maturity
σ = volatility of the asset

Assumptions Made for this Calculator

It works on European options that can only be exercised at expiration.
No dividends paid out during the option’s life.
No transaction and commissions costs in buying the option.
The returns on the underlying are normally distributed.

# How to Run
## In Docker Container
**Requirement**: Docker must be installed locally. More info here https://docs.docker.com/get-docker/

Run following command from terminal
```sh run_in_docker.sh```

# How to Run
## In Docker Container
**Requirement**: python >= 3.7.*

Run following command from terminal
```sh run_local.sh```

# API Documentation
once API server is up and running, go to following url for API documentation and testing
http://127.0.0.1:8000/docs


