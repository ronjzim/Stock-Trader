import schedule
import time
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest, OrderRequest
from alpaca.trading.enums import AssetClass, OrderType, OrderSide, TimeInForce
from alpaca.data import StockHistoricalDataClient, StockTradesRequest, StockBarsRequest, TimeFrame
from datetime import datetime, timedelta
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

# Enter your Alpaca API key and secret here
API_KEY = os.getenv('API_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')

trading_client = TradingClient(API_KEY, SECRET_KEY)
data_client = StockHistoricalDataClient(API_KEY, SECRET_KEY)

# Check account information, run program
def run_trading_bot():
    account = trading_client.get_account()
    if account.trading_blocked:
        print('Account is currently restricted from trading.')
    else:
        print(f'${account.buying_power} is available as buying power.')

# Get a list of portfolio assets
portfolio = trading_client.get_all_positions()
portfolio_symbols = [position.symbol for position in portfolio]
print(portfolio)

# search for US equities assets to work with (optional, way longer run time)
search_params = GetAssetsRequest(asset_class=AssetClass.US_EQUITY)
# assets = trading_client.get_all_assets(search_params)
# asset_symbols = [asset.symbol for asset in assets if asset.tradable and asset.symbol not in portfolio_symbols]

# S&P 500 sample symbols (faster run time, good to start with)
stock_symbols = ["AAPL", "MSFT", "AMZN", "GOOGL", "GOOG", "NVDA", "BRK.B", "TSLA", "META", "UNH", "JNJ", "XOM", "V", "PG", "JPM", "MA", "HD", "MRK", "CVX", "LLY", "PEP", "ABBV", "KO", "AVGO", "COST", "MCD", "TMO", "WMT", "CSCO", "ACN", "NEE", "NKE", "PFE", "ADBE", "NFLX", "ABT", "CRM", "TXN", "LIN", "DIS", "PM", "VZ", "CMCSA", "DHR", "HON", "WFC", "MS", "BMY", "RTX", "UNP", "INTC", "MDT", "IBM", "SCHW", "GS", "GE", "LMT", "AMD", "UPS", "T", "LOW", "AXP", "ISRG", "ORCL", "SPGI", "PLD", "AMGN", "AMT", "SYK", "ELV", "CVS", "MDLZ", "CAT", "ZTS", "GILD", "ADP", "BKNG", "DE", "CI", "BLK", "CB", "BA", "MMC", "C", "DUK", "TJX", "MO", "PYPL", "TGT", "PNC", "BDX", "SO", "USB", "VRTX", "MMM", "MU", "REGN", "AMAT", "ITW", "ADI", "EQIX", "CCI", "CL", "EW", "NSC", "FCX", "BSX", "APD", "CME", "ICE", "COP", "ADM", "MCO", "HUM", "SPG", "ADSK", "NOW", "CTVA", "GM", "TRV", "FIS", "AON", "SNPS", "SBUX", "KMB", "MPC", "ORLY", "MCK", "TROW", "AEP", "HCA", "MET", "CMG", "DG", "AIG", "PSA", "EMR", "GD", "ILMN", "D", "FDX", "STZ", "SRE", "EXC", "PSX", "ETN", "COF", "APTV", "ROP", "DLR", "EBAY", "YUM", "PGR", "WBA", "ROST", "KMI", "WMB", "CTAS", "NOC", "EOG", "WELL", "ALL", "HSY", "DOW", "PH", "MSCI", "KLAC", "PPG", "OXY", "DGX", "XEL", "ED", "BIIB", "FTNT", "IDXX", "SBAC", "ODFL", "NUE", "ANSS", "CDNS", "A", "DFS", "RSG", "FAST", "PAYC", "CSX", "RMD", "CRL", "AVB", "STT", "TEL", "KEYS", "MLM", "FTV", "ETSY", "HPE", "RHI", "CNP", "PXD", "ESS", "MOS", "SWK", "TDG", "LDOS", "LHX", "VTR", "TRU", "AAL", "HAL", "MTD", "RF", "TSN", "AES", "BF.B", "HST", "ETR", "VMC", "VRSN", "CTLT", "HES", "FTI", "F", "PFG", "NRG", "WRB", "NTRS", "ALB", "LNC", "ZBH", "CPRT", "UDR", "AKAM", "EXPE", "URI", "CFG", "TTWO", "WYNN", "IR", "NTAP", "CINF", "ZION", "NWS", "FMC", "CMA", "CAG", "SWKS", "CF", "HP", "LKQ", "BWA", "SYY", "TXT", "JCI", "GLW", "NCLH", "WY", "JWN", "ROL", "JBHT", "KMX", "HOG", "AAP", "ALK", "RL", "NDAQ", "MRO", "PRGO", "KSS", "HSIC", "IRM", "WU", "LUV", "COTY", "PENN", "NI", "UAL", "CZR", "MGM", "HBI", "DVA", "AIZ", "HII", "UHS", "HOLX", "BKR", "HAS", "LEG", "XRAY", "PNR", "HRL", "BBY", "DISH", "PWR", "WHR", "J", "QRVO", "FLT", "HIG", "EQR", "DRI", "LYB", "ALGN", "TPR", "ATO", "L", "DOV", "CBOE", "KIM", "CNC", "FRT", "CPT", "GRMN", "SEE", "NTES", "VFC", "LUMN", "VRSK", "CMS", "ZBRA", "MSM", "AVY", "FFIV", "JNPR", "BAX", "ULTA", "GWW"]
asset_symbols = [stock for stock in stock_symbols if stock not in portfolio_symbols]

# get historical data
def get_historical_data(symbol, start, end):
    request_params = StockBarsRequest(
        symbol_or_symbols = [symbol],
        timeframe = TimeFrame.Day,
        start = start,
        end = end,
    )

    bars = data_client.get_stock_bars(request_params)
    return bars.df

# Check performance function
def check_performance(symbol):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)  # 1 year of stock data

    # Get historical data
    stock_df = get_historical_data(symbol, start_date, end_date)
    
    # If the DataFrame is empty, return False
    if stock_df.empty:
        print(f"No data found for {symbol}.")
        return False
    
    # Calculate performance
    stock_df['Daily Return'] = stock_df['close'].pct_change()
    stock_df['3 Month Return'] = stock_df['close'].pct_change(periods=63)  # 3 months
    stock_df['1 Month Return'] = stock_df['close'].pct_change(periods=21)  # 1 month
    stock_df['1 Week Return'] = stock_df['close'].pct_change(periods=5)    # 1 week
    stock_df['1 Year Return'] = stock_df['close'].pct_change(periods=252)  # 1 year

    # Check if the stock is up 5% in a day
    if stock_df['Daily Return'].iloc[-1] >= 0.05:
        # Check other performance conditions
        if (stock_df['1 Year Return'].iloc[-1] < 0 and 
            stock_df['3 Month Return'].iloc[-1] > 0 and
            stock_df['1 Month Return'].iloc[-1] > 0 and
            stock_df['1 Week Return'].iloc[-1] > 0):
            return True

    return False

# Check performance function for selling
def check_performance_for_selling(symbol):
    # Get last close price and the average buy price
    position = next((pos for pos in portfolio if pos.symbol == symbol), None)
    if not position:
        return False

    last_close_price = float(position.current_price)
    avg_buy_price = float(position.avg_entry_price)
    percent_change = ((last_close_price - avg_buy_price) / avg_buy_price) * 100

    if percent_change >= 5.01 or percent_change <= -4.98:
        return True
    return False

# Determine which US equities / S&P 500 assets meet the criteria
eligible_assets_for_buying = []
for symbol in asset_symbols:
    if check_performance(symbol) and symbol not in portfolio_symbols:
        eligible_assets_for_buying.append(symbol)
        print(f"{symbol} meets the criteria.")

if not eligible_assets_for_buying:
    print("No assets meet the criteria for purchase today.")
else:
    print("Eligible assets for purchase today:", eligible_assets_for_buying)

# Determine which assets in the current portfolio to sell
eligible_assets_for_selling = []
for symbol in portfolio_symbols:
    if check_performance_for_selling(symbol):
        eligible_assets_for_selling.append(symbol)
        print(f"{symbol} meets the criteria for selling.")

if not eligible_assets_for_selling:
    print("No assets in the portfolio meet the criteria for selling.")
else:
    print("Eligible assets for selling today:", eligible_assets_for_selling)

# Buy the eligible assets for buying
for symbol in eligible_assets_for_buying:
    qty_to_buy = 10  # Adjust the quantity of shares to by as needed
    order_request = OrderRequest(
        symbol=symbol,
        qty=qty_to_buy,
        side=OrderSide.BUY,
        type=OrderType.MARKET,
        time_in_force=TimeInForce.GTC
    )
    trading_client.submit_order(order_request)
    print(f"Placed buy order for {symbol}.")

# Sell the eligible assets for selling
for symbol in eligible_assets_for_selling:
    position = next((pos for pos in portfolio if pos.symbol == symbol), None)
    if position:
        qty_to_sell = position.qty
        order_request = OrderRequest(
            symbol=symbol,
            qty=qty_to_sell,
            side=OrderSide.SELL,
            type=OrderType.MARKET,
            time_in_force=TimeInForce.GTC
        )
        trading_client.submit_order(order_request)
        print(f"Placed sell order for {symbol}.")

# Schedule the script to run every weekday at 9:30 AM
schedule.every().monday.at("09:30").do(run_trading_bot)
schedule.every().tuesday.at("09:30").do(run_trading_bot)
schedule.every().wednesday.at("09:30").do(run_trading_bot)
schedule.every().thursday.at("09:30").do(run_trading_bot)
schedule.every().friday.at("09:30").do(run_trading_bot)

while True:
    schedule.run_pending()
    time.sleep(1)