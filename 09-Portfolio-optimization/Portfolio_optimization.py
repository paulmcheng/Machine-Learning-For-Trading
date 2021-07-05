import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm 

def normalize(df):
    return df / df.iloc[0,:]

def find_portfolio_statistics(allocs, df, gen_plot = False):
    '''
    Compute portfolio statistics 
    1) Cumulative return 
    2) Daily return 
    3) Average daily return 
    4) Standard deviation of the daily returns
    5) Annual sharpe ratio
    6) Final value 
    7) Total returns 

    allocs: list of allocation fractions for each stock
            eg [0.5, 0.5, 0.35, 0.15] # total equal to 1
    df: DataFrame with the data 
    gen_plot(optional): If True, plot performance of the allocation compared to SPY500
                
    '''
    # number of business day per year 
    businessday = 252
    symbol = 'APPL'
    dfcopy = df.copy()

    # normalization 
    df = (df / df.iloc[0])
    # allocation of the resources
    df = df * allocs
    # sum of the value of the resources 
    df = df.sum(axis = 1)

    # compute portfolio statistics 

    # cumulative return 
    cumreturn = (df.iloc[-1] / df.iloc[0]) - 1

    # daily returns 
    dailyreturns = (df.iloc[1:] / df.iloc[:-1].values) - 1
    avedailyreturns = dailyreturns.mean(axis = 0)
    yearlyreturns = avedailyreturns 

    # standard deviation of the daily returns
    stddailyreturns = dailyreturns.std(axis = 0)

    # Sharpe ratio
    sharperatio = (businessday ** (0.5)) * ((avedailyreturns - 0 ) /  stddailyreturns)
    endingvalues = df.iloc[-1]
    totalreturns = avedailyreturns 

    if gen_plot == True:
        #plot portfolio
        dfcopynormed = dfcopy[symbol] / dfcopy[symbol].iloc[0]
        ax = dfcopynormed.plot(title = 'Daily portfolio value and {}'.Format(symbol), label = symbol)
        sumcopy = dfcopy.sum(axis = 1)
        normed = sumcopy/sumcopy.iloc[0]
        normed.plot(label='Portfolio value', ax = ax)
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        ax.legend(loc = 2)
        plt.show()

    print('For allocation as follows:')
    print(allocs)
    print('Annualized Sharpe ratio:')
    print(sharperatio)

    return yearlyreturns, stddailyreturns, sharperatio











