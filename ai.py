import requests
import pandas as pd
import numpy as np

# Define the Binance API endpoint
api_endpoint = "https://api.binance.com"

# Get the highest volume pairs traded on Spot markets
response = requests.get(api_endpoint + "/api/v1/ticker/24hr")
pairs = response.json()

# Sort the pairs by volume
pairs.sort(key=lambda x: -float(x['volume']))

# Select the top 10 pairs
top_pairs = pairs[:10]

# Create a dictionary to store the historical data for each pair
historical_data = {}

# For each pair, get the 5-minute historical data
for pair in top_pairs:
    symbol = pair['symbol']
    response = requests.get(api_endpoint + f"/api/v1/klines?symbol={symbol}&interval=5m")
    data = response.json()
    
    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(data, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])
    
    # Convert the time columns to datetime
    df['Open time'] = pd.to_datetime(df['Open time'], unit='ms')
    df['Close time'] = pd.to_datetime(df['Close time'], unit='ms')
    
    # Convert the price and volume columns to float
    df['Open'] = df['Open'].astype(float)
    df['High'] = df['High'].astype(float)
    df['Low'] = df['Low'].astype(float)
    df['Close'] = df['Close'].astype(float)
    df['Volume'] = df['Volume'].astype(float)
    
    # Store the DataFrame in the dictionary
    historical_data[symbol] = df

# Calculate a correlation matrix based on the historical data
correlation_matrix = pd.DataFrame()

for symbol, df in historical_data.items():
    correlation_matrix[symbol] = df['Close']

correlation_matrix = correlation_matrix.corr()

print(correlation_matrix)