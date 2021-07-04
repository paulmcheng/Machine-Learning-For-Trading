import pandas as pd
import matplotlib.pyplot as plt
import stockdata as sd

def compute_daily_return(df):
    #compute daily return using pandas' dataframe
    dailyreturns = (df/df.shift(1)) - 1
    daily_returns.iloc[0,:] = 0    
    # compute daily return values 
    #dailyreturns = df.copy() #copy dataframe
    # compute daily returns for row 1 onwards
    #dailyreturns[1:] = (df[1:]/df[:-1].values) - 1
    # set daily returns for the first row
    #dailyreturns.iloc[0,:] = 0
    return dailyreturns

def compute_cumulative_return(df):
    # compute the % return since day 1 
    cumreturns = (df/df.iloc[0, :]) - 1
    return cumreturns

def test_run():
    # compute daily retrun 

    # read data 
    dates = pd.date_range('2017-04-01', '2018-03-01')
    symbol = 'AAPL'
    symbols = [symbol]
    df = sd.get_data(symbols, dates)

    # access the underlying ndarray in dataframe .values
    dailyret = (df[symbol][1:]/df[symbol][:-1].values - 1) * 100

    #plot daily return data, retain axis object
    ax = dailyret.plot(title='{} daily return'.format(symbol), label=symbol)
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("% Return", fontsize=12)
    ax.legend(loc='lower left')
    plt.show()

if __name__ == "__main__":
    test_run()