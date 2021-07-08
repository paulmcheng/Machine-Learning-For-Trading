import pandas as pd
import datetime
from tqdm import tqdm
import yfinance as yf

tickers = ['APPL', 'SPY' , 'IBM', 'GOOG', 'TSLA', 'GLD', 'IBM', 'PSX', 'XOM']

for ticker in tqdm(tickers):
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days = 365 * 5.0)
    data = yf.download('SPY', start = start_date, end= end_date)
    df=pd.DataFrame(data)
    df.to_csv("{}.csv".format(ticker))
