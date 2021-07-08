import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm 
import sys
from pathlib import Path as pa
sys.path.insert(0, str(pa(__file__).resolve().parent.parent))
from common import stockdata as sd

def normalize(df):
    return df / df.iloc[0,:]

def find_portfolio_statistics(allocs, df, gen_plot = False):
    '''
    allocs: list of allocation fractions for each stock
            eg [0.5, 0.5, 0.35, 0.15] # total equal to 1
    df: DataFrame with the data 
    gen_plot(optional): If True, plot performance of the allocation compared to SPY500

    Output portfolio statistics 
    1) Annual return
    2) Standard deviation of the annual returns
    3) Sharpe ratio
      
    '''
    # number of business day per year 
    businessday = 252
    symbol = 'SPY' #S&P 500 Trust ETF
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
    yearlyreturns = avedailyreturns * businessday

    # standard deviation of the daily returns
    stddailyreturns = dailyreturns.std(axis = 0)
    stdyearlyreturns = yearlyreturns.std(axis = 0)

    # Sharpe ratio
    sharperatio = (businessday ** (0.5)) * ((avedailyreturns - 0 ) /  stddailyreturns)

    if gen_plot == True:
        #plot portfolio
        dfcopynormed = dfcopy[symbol] / dfcopy[symbol].iloc[0]
        ax = dfcopynormed.plot(title = 'Daily portfolio value and {}'.format(symbol), label = symbol)
        sumcopy = dfcopy.sum(axis = 1)
        normed = sumcopy/sumcopy.iloc[0]
        normed.plot(label='Portfolio value', ax = ax)
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        ax.legend(loc = 2)
        plt.show()

    return yearlyreturns, stdyearlyreturns, sharperatio

def generate_random_portfolios(nportfolio, symbols):
        
    dates = pd.date_range('2017-04-01', '2018-02-28')
    df = sd.get_data(symbols, dates)

    # number of stocks 
    nstock = len(symbols)

    # initialization the final result matrix with zeros
    resultmatrix = np.zeros([nportfolio,3])

    for i in tqdm(range(nportfolio)):
         random = np.random.random(nstock)
         allocs = random/np.sum(random)
         meanreturn, stdreturn, sharperatio = find_portfolio_statistics(allocs, df, gen_plot=False)
         resultmatrix[i, 0] = meanreturn
         resultmatrix[i, 1] = stdreturn
         resultmatrix[i, 2] = sharperatio

    return resultmatrix

if __name__ == "__main__":

    symbols = ['SPY', 'AAPL', 'GOOG', 'IBM']

    resultmatrix = generate_random_portfolios(1000, symbols)    

    # convert results array to Pandas DataFrame
    resultframe = pd.DataFrame(resultmatrix, columns=['ret','stdev','sharpe'])

    #create scatter plot by sharpe ratio
    plt.scatter(resultframe.stdev, resultframe.ret,c=resultframe.sharpe,cmap='RdYlBu')
    plt.ylabel('Annualized mean return')
    plt.xlabel('Standard deviation')
    plt.title('Coefficient frontier')

    cb = plt.colorbar()
    cb.set_label("Sharpe ratio")  

    plt.show()