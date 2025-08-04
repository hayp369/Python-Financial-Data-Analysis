# Python-Financial-Data-Analysis

# Project Overview

This repository contains two Python scripts designed to perform automated financial data analysis using the Supertrend indicator. The programs fetch weekly stock data, calculate trend indicators, and provide real-time notifications via a Telegram bot. The supertrend calculations still needs work. 

# Scripts Included

WORKINGNASDAQStockScreener.py: 

This script fetches historical stock data for a list of NASDAQ-listed companies, calculates the Supertrend indicator, and determines if a stock is in an "Uptrend". It then calculates how far the latest closing price is from the Supertrend's "support" level and sends a message with this information to a specified Telegram channel. The script also saves the list of stocks currently in an uptrend to a text file.

WORKINGNYSEStockScreenerPrgm.py:

Similar to the NASDAQ screener, this program performs the same analysis for a list of stocks from the New York Stock Exchange (NYSE). It fetches data, calculates the Supertrend, identifies uptrends, and sends percentage-away-from-support notifications to Telegram. The list of NYSE stocks in an uptrend is also saved to a file.

# Key Features

Financial Indicator Analysis:

The scripts compute the Supertrend indicator using pandas and numpy to identify market trends.

API Integration: 

The programs use the requests library to send automated, formatted messages to a Telegram chat, providing instant notifications.

Data Handling: 

The scripts utilize the yahoo_fin library to retrieve historical stock data and process it using the pandas library.

File I/O: 

The programs can load stock symbols from a text file and save the results of the scan to a new file, demonstrating practical file handling skills.

# Getting Started

Prerequisites

Python 3.x

The following Python libraries:

pandas

numpy

yahoo_fin

requests

You can install these dependencies using pip:

pip install pandas numpy yahoo_fin requests

# Configuration

Telegram Bot Setup:

You will need to create a Telegram bot and get your bot token and chat ID. Replace the placeholder values for TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in both scripts with your actual credentials.

Stock Lists: 

Create a text file (e.g., NYSEStocks.txt and NASDAQStocks.txt) containing the stock tickers you want to scan, with each ticker on a new line. Update the file paths in the scripts to point to your files.

