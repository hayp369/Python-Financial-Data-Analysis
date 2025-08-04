import pandas as pd
import numpy as np
from yahoo_fin import stock_info as si
import time
import requests

# Replace with your Telegram bot token and chat ID
TELEGRAM_BOT_TOKEN = "*************************"
TELEGRAM_CHAT_ID = "**********"

def send_telegram_message(message):
    """Sends a message to the specified Telegram chat."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to send Telegram message: {e}")

# Send a test message to the Telegram bot
send_telegram_message("Test message: The program has started successfully!")

def get_weekly_data(ticker):
    """Fetches weekly historical data for a given stock"""
    df = si.get_data(ticker, interval='1wk')
    return df[['open', 'high', 'low', 'close']]

def calculate_supertrend(df, period=10, multiplier=1.7):
    """Computes the Supertrend indicator."""

    df['H-L'] = df['high'] - df['low']
    df['H-PC'] = np.abs(df['high'] - df['close'].shift(1))
    df['L-PC'] = np.abs(df['low'] - df['close'].shift(1))
    df['TR'] = df[['H-L', 'H-PC', 'L-PC']].max(axis=1)
    df['ATR'] = df['TR'].rolling(window=period).mean()

    df['Upper Band'] = (df['high'] + df['low']) / 2 + multiplier * df['ATR']
    df['Lower Band'] = (df['high'] + df['low']) / 2 - multiplier * df['ATR']

    df['final_upper_band'] = df['Upper Band']
    df['final_lower_band'] = df['Lower Band']
    df['Supertrend'] = 0.0

    for i in range(1, len(df.index)):
        curr, prev = df.index[i], df.index[i - 1]
        if df.loc[prev, 'Supertrend'] == 0.0:  # Ensuring the first row is initialized correctly
            df.loc[prev, 'Supertrend'] = df.loc[prev, 'final_lower_band']

        if df.loc[curr, 'close'] > df.loc[prev, 'final_upper_band']:
            df.loc[curr, 'Supertrend'] = df.loc[curr, 'final_lower_band']
        elif df.loc[curr, 'close'] < df.loc[prev, 'final_lower_band']:
            df.loc[curr, 'Supertrend'] = df.loc[curr, 'final_upper_band']
        else:
            df.loc[curr, 'Supertrend'] = df.loc[prev, 'Supertrend']
            if df.loc[curr, 'Supertrend'] == df.loc[prev, 'final_upper_band'] and df.loc[curr, 'close'] > df.loc[curr, 'final_upper_band']:
                df.loc[curr, 'Supertrend'] = df.loc[curr, 'final_lower_band']
            if df.loc[curr, 'Supertrend'] == df.loc[prev, 'final_lower_band'] and df.loc[curr, 'close'] < df.loc[curr, 'final_lower_band']:
                df.loc[curr, 'Supertrend'] = df.loc[curr, 'final_upper_band']

    df['Trend'] = np.where(df['close'] > df['Supertrend'], 'Uptrend', 'Downtrend')

    return df[['close', 'Supertrend', 'final_upper_band', 'final_lower_band', 'Trend']]

def scan_stocks_for_support(stock_list):
    """Scans stocks and notifies the percent away the price is from the blue 'support' on the weekly timeframe only for stocks in an uptrend."""
    uptrend_stocks = []
    results = []
   
    for stock in stock_list:
        try:
            print(f"Fetching data for {stock}...")
            df = get_weekly_data(stock)
           
            if df.empty:
                print(f"No data available for {stock}. Skipping...")
                continue  # Skip if data is empty
           
            df = df.dropna()
            supertrend_df = calculate_supertrend(df)  # Get Supertrend data
           
            if supertrend_df.empty:
                print(f"Not enough data for {stock}. Skipping...")
                continue  # Skip if not enough data
           
            df = df.join(supertrend_df, rsuffix='_new')  # Merge Supertrend with original data
            latest_close = df['close'].iloc[-1]  # Get the latest close price
            latest_trend = df['Trend_new'].iloc[-1]  # Get the latest trend value

            if latest_trend == 'Uptrend':
                latest_lower_band = df['final_lower_band'].iloc[-1]  # Get the latest lower band (support)

                # Calculate the percent away from the support
                percent_away = ((latest_close - latest_lower_band) / latest_lower_band) * 100
                
                result = f"{stock} is {percent_away:.2f}% away from the blue 'support' (lower band) and is currently in an uptrend."
                results.append(result)
                print(result)
                send_telegram_message(result)

                # Format the stock ticker with exchange for saving
                exchange = 'NASDAQ' if 'NASDAQ' in stock else 'NYSE'
                uptrend_stocks.append(f"{exchange}:{stock}")
            else:
                print(f"{stock} is not in an uptrend.")
           
        except Exception as e:
            print(f"Error processing {stock}: {e}")
       
        time.sleep(1)  # Prevents excessive API requests
   
    return uptrend_stocks

def load_stock_list(file_path):
    """Loads a list of stock symbols from a text file."""
    try:
        with open(file_path, 'r') as file:
            stock_list = [line.strip() for line in file.readlines()]
        return stock_list
    except Exception as e:
        print(f"Error loading stock list: {e}")
        return []

def save_uptrend_stocks(file_path, stocks):
    """Saves the list of uptrend stocks to a text file."""
    try:
        with open(file_path, 'w') as file:
            file.write(",".join(stocks))
        print(f"Uptrend stocks saved to {file_path}")
    except Exception as e:
        print(f"Error saving uptrend stocks: {e}")

# Assuming you have a valid 'Stocks.txt' file
stock_list = load_stock_list(r"C:*****************")

# Run the stock scanning process for support levels
uptrend_stocks = scan_stocks_for_support(stock_list)
print("Uptrend stocks:", uptrend_stocks)

# Save the uptrend stocks to a file
save_uptrend_stocks(r"C:*******************", uptrend_stocks)
