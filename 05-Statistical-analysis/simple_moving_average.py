import os
import pandas as pd
import matplotlib.pyplot as plt

def symbol_to_path(symbol, base_dir="../data"):
    #Return CSV path for the ticker
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))   

def get_data(symbols, dates):
     #Read stock data from for given symbols from CSV file
     df = pd.DataFrame(index=dates)

     for symbol in symbols:
         df_temp = pd.read_csv(symbol_to_path(symbol), 
         index_col='Date', 
         parse_dates = True, 
         usecols=['Date', 'Adj Close'],
         na_values=['nan'])
         df_temp = df_temp.rename(columns={'Adj Close' : symbol})
         df = df.join(df_temp)
         #remove NA in the data 
         df = df.dropna(subset=[symbol])

     return df

def plot_data(df, title="stock prices"):
    # Plot stock prices 
    fontsize = 12
    ax = df.plot(title=title, fontsize=fontsize)
    ax.set_xlabel("Date", fontsize=fontsize)
    ax.set_ylabel("Price", fontsize=fontsize)
    plt.show()

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
    df = get_data(symbols, dates)

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