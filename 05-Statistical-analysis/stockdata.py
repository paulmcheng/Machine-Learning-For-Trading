import os
import pandas as pd

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