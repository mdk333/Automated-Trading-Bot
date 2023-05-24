from alpaca_trade_api.rest import REST, TimeFrame
from pymongo import MongoClient

# Connect to the Alpaca API
api = REST('YOUR_API_KEY_ID', 'YOUR_SECRET_KEY', base_url='https://paper-api.alpaca.markets')

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['trade_bot_db']
