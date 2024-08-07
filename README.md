Stock Trading Bot:

This Project is a Python Stock Trading Bot built in Python using the Alpaca trading API.

Usage:
Enter your Alpaca API_KEY and SECRET_KEY in the designated portion of the file. The Bot will connect to your live or paper Alpaca
portfolio depending on the API and SECRET KEYs you have entered. The Bot is designed to Scan through the S&P 500 US equities daily 
and automatically buy and sell shares based on set parameters.

Shares bought and Stocks scanned are configurable

Buying Parameters:
A stock will be purchased if the daily return is greater than or equal to 5%, the 1 week, 1 month, and 3 month return is positive, but
the 1 year return is negative.

Selling Parameters:
A stock from the portfolio will be sold if it has gained more than 5% in value since its purchase, or has lost more than 4.98% in value
since its purchase.
