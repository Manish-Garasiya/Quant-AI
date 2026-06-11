from src.data_loader import load_data
import pandas as pd
import matplotlib.pyplot as plt

# -- Loading the stock data and saving it to a csv file --
symbol = str(input("Enter ticker symbol for the stock : "))
# data = load_data(symbol)
csv_name = f'{symbol}_data.csv'
# data.to_csv(csv_name)

# -- Reading the csv file and preparing the data for plotting --
df = pd.read_csv(csv_name)
df = df.iloc[1:]
df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
df['Price'] = pd.to_datetime(df['Price'])
# ------ Plotting the stock price curve ------

# plt.plot(df['Price'], df['Close'],color='blue')
# plt.title("Stock price curve")
# plt.ylabel('Closing price')
# plt.xlabel('Date')
# plt.grid(True)

df['Returns'] = df['Close'].pct_change()
df['MA20'] = df['Close'].rolling(window=20).mean()
df['MA50'] = df['Close'].rolling(window=50).mean()

plt.plot(df['Price'], df['Close'], color='blue')
plt.plot(df['Price'], df['MA20'], color='red')
plt.plot(df['Price'], df['MA50'], color='green')
plt.show()
