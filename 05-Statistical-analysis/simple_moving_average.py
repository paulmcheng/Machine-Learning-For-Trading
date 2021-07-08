import pandas as pd
import matplotlib.pyplot as plt
import sys
from pathlib import Path as pa
sys.path.insert(0, str(pa(__file__).resolve().parent.parent))
from common import stockdata as sd

def get_rolling_mean(df, window):
     return df.rolling(window=window, center=False).mean()

def get_rolling_std(df, window):
    return df.rolling(window=window, center=False).std()

def get_bollinger_bands(rmean, rstd):
    # create the bollinger bands of 2 standard deviration from the mean    
    return rmean+2*rstd, rmean-2*rstd

def test_run():
    # compute rolling mean

    #Read data
    dates = pd.date_range('2017-04-01', '2018-02-28')
    symbol='AAPL'
    symbols = [symbol]
    df = sd.get_data(symbols, dates)

    # compute rolling mean
    rmean = get_rolling_mean(df[symbol], window=20)

    # compute rolling standard deviation
    rstd = get_rolling_std(df[symbol], window=20)

    # compute upper and lower bands
    upper_band, lower_band = get_bollinger_bands(rmean, rstd)

    #plot
    ax2 = df[symbol].plot(title='{} stock price on Bollinger bands'.format(symbol) , label='Price', color="black")
    rmean.plot(label='Rolling mean', ax=ax2, color='gray')
    upper_band.plot(label='Upper band', ax=ax2, color='green')
    lower_band.plot(label='Lower band', ax=ax2, color='red')

    ax2.set_xlabel("Date")
    ax2.set_ylabel("Price")
    ax2.legend(loc='upper left')
    plt.show()

if __name__ == "__main__":
    test_run()