import yfinance as yf
import pandas as pd

def get_stock_data(symbol: str) -> dict:
    try:
        stock = yf.Ticker(symbol)
        current_price = stock.info['regularMarketPrice']
        return {
            'symbol': symbol,
            'current_price': current_price,
            'name': stock.info['longName'],
            'currency': stock.info['currency']
        }
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return None

def calculate_portfolio_value(holdings):
    total_value = 0
    for holding in holdings:
        stock_data = get_stock_data(holding['symbol'])
        if stock_data:
            value = holding['shares'] * stock_data['current_price']
            total_value += value
    return total_value
