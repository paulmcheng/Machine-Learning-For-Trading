import pandas as pd 
import matplotlib.pyplot as plt

# plot two columns in the same plot 
df = pd.read_csv("../data/AAPL.csv")
df[['Close', 'Adj Close']].plot()
plt.show() 