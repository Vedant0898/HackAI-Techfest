import requests
import os

import dotenv

dotenv.load_dotenv()

BASE_URL = "https://api.currencyapi.com/v3/latest"
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

assert ACCESS_TOKEN is not None, "ACCESS_TOKEN not found in environment variables"


# Function to handle API call for exchange rates
def get_exchange_rates(base_cur, symbols):
    url = f'{BASE_URL}?apikey={ACCESS_TOKEN}&currencies={"%2C".join(symbols)}&base_currency={base_cur}'

    res = requests.get(url)
    if res.status_code == 200:
        d = {}
        r = res.json()
        for sym in r["data"].keys():
            d[sym] = r["data"][sym]["value"]
        return True, d
    else:
        return False, res.json()["message"]
