import json
import streamlit as st
import os
import requests
from typing import List

st.set_page_config(page_title="This is a Multipage WebApp")
st.sidebar.success("Select Any Page from here")

ACCESS_TOKEN = "cur_live_aDyyqOV1xkgTPvUSdp3743MvF7d4gPqPe6qw6wTg"
BASE_URL = "https://api.currencyapi.com/v3/latest"

CURRENCIES = [
    "AED",
    "AFN",
    "ALL",
    "AMD",
    "ANG",
    "AOA",
    "ARS",
    "AUD",
    "AWG",
    "AZN",
    "BAM",
    "BBD",
    "BDT",
    "BGN",
    "BHD",
    "BIF",
    "BMD",
    "BND",
    "BOB",
    "BRL",
    "BSD",
    "BTN",
    "BWP",
    "BYN",
    "CZK",
    "DJF",
    "DKK",
    "DOP",
    "DZD",
    "EGP",
    "ERN",
    "ETB",
    "EUR",
    "FJD",
    "FKP",
    "GBP",
    "GEL",
    "GGP",
    "GHS",
    "GIP",
    "GMD",
    "GNF",
    "GTQ",
    "GYD",
    "HKD",
    "HNL",
    "HRK",
    "HTG",
    "HUF",
    "IDR",
    "ILS",
    "IMP",
    "INR",
    "IQD",
    "IRR",
    "ISK",
    "JEP",
    "JMD",
    "JOD",
    "JPY",
    "KES",
    "KGS",
    "KHR",
    "KMF",
    "KPW",
    "KRW",
    "KWD",
    "KYD",
    "KZT",
    "LAK",
    "LBP",
    "LKR",
    "LRD",
    "LSL",
    "LTL",
    "LVL",
    "LYD",
    "MAD",
    "MDL",
    "MGA",
    "MKD",
    "MMK",
    "MNT",
    "MOP",
    "MRO",
    "MUR",
    "MVR",
    "MWK",
    "MXN",
    "MYR",
    "MZN",
    "NAD",
    "NGN",
    "NIO",
    "NOK",
    "NPR",
    "NZD",
    "OMR",
    "PAB",
    "PEN",
    "PGK",
    "PHP",
    "PKR",
    "PLN",
    "PYG",
    "QAR",
    "RON",
    "RSD",
    "RUB",
    "RWF",
    "SAR",
    "SBD",
    "SCR",
    "SDG",
    "SEK",
    "SGD",
    "SHP",
    "SLL",
    "SOS",
    "SRD",
    "STD",
    "SVC",
    "SYP",
    "SZL",
    "THB",
    "TJS",
    "TMT",
    "TND",
    "TOP",
    "TRY",
    "TTD",
    "TWD",
    "TZS",
    "UAH",
    "UGX",
    "USD",
    "UYU",
    "UZS",
    "VEF",
    "VND",
    "VUV",
    "WST",
    "XAF",
    "XAG",
    "XAU",
    "XCD",
    "XDR",
    "XOF",
    "XPF",
    "YER",
    "ZAR",
    "ZMK",
    "ZMW",
    "ZWL",
    "XPT",
    "XPD",
    "BTC",
    "ETH",
    "BNB",
    "XRP",
    "SOL",
    "DOT",
    "AVAX",
    "MATIC",
    "LTC",
    "ADA",
    "USDT",
    "USDC",
    "DAI",
    "BUSD",
    "ARB",
    "OP",
]


def get_exchange_rates(base_cur: str, symbols: List[str]):
    url = f'{BASE_URL}?apikey={ACCESS_TOKEN}&currencies={"%2C".join(symbols)}&base_currency={base_cur}'

    res = requests.get(url)
    # print(res)
    if res.status_code == 200:
        d = {}
        r = res.json()
        for sym in r["data"].keys():
            d[sym] = r["data"][sym]["value"]
        # print(d)
        return True, d
    else:
        # print(res.json())
        return False, res.json()["errors"]


if "userdata.json" in os.listdir():
    with open("userdata.json", "r") as openfile:
        json_object = openfile.readlines()
    if len(json_object) == 0:
        st.write("Please create new registry")
    else:
        with open("userdata.json", "r") as openfile:
            json_object = json.load(openfile)
            name = json_object["name"]
            email = json_object["email"]
            base_currency = json_object["base_currency"]
            target_currency = json_object["target_currency"]
            st.title("Welcome {0}".format(name))
            st.write("Your email address is : {0}".format(email))
            st.write("Your base currency is set to {0}".format(base_currency))
            # r = get_exchange_rates("INR", ["USD", "EUR", "CAD"])
            # st.write(r)
            for i in target_currency:
                mini = list(i.values())
                print(mini)
                r, y = get_exchange_rates(base_currency, list(i.keys()))
                st.write(
                    "{0} -> min {1}, max {2}, current value {3}".format(
                        list(i.keys())[0],
                        list(i.values())[0][0],
                        list(i.values())[0][1],
                        list(y.values())[0],
                    )
                )

else:
    st.write("Please create new registry")
