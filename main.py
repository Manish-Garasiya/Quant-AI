from src.data_loader import load_data
from src.Indicators import MACD,calculate_DIs_and_ADX
from src.Strategy import signal
from src.execution import execute
from src.Performance import performance
import matplotlib.pyplot as plt

def main():
    print("Loading the data....")
    data = load_data("INFY.NS","1y","1d")

    print("Calculating the Indicators ...")
    data['macd'] = MACD(data['Close'])
    data['signal_line'] = data['macd'].ewm(span=9, adjust=False).mean()
    data['di_plus'],data['di_minus'],data['adx'] = calculate_DIs_and_ADX(data['High'],data['Low'],data['Close'])
    data['ema_100'] = data['Close'].ewm(span=100, adjust=False).mean()
    print("Applying Strategy logic ....")
    data = signal(data)

    print("Executing the trade .....")
    data = execute(data)

    print("Calculating Results ....\n")
    results = performance(data)
    results = results.T
    print(results)

    print("Plotting the curves/graphs....")

    #P and L graph
    data[['delta']].plot(figsize = (10,6))
    plt.title("P & L Graphs")
    plt.xlabel("Date")
    plt.ylabel("Profit or loss(in ₹)")
    plt.grid(True)
    plt.show()

    #plotting drawdown graph
    data[['drawdown']].plot(figsize = (10,6))
    plt.title("Drawdown graph")
    plt.xlabel('Date')
    plt.ylabel('Drawdown')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()

