import json
import streamlit as st
import os
import requests
from typing import List
st.set_page_config(page_title = "This is a Multipage WebApp") 
st.sidebar.success("Select Any Page from here") 

ACCESS_TOKEN = "cur_live_aDyyqOV1xkgTPvUSdp3743MvF7d4gPqPe6qw6wTg"
BASE_URL = "https://api.currencyapi.com/v3/latest"

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

if ('userdata.json' in os.listdir()):
    with open('userdata.json', 'r') as openfile:
       json_object = openfile.readlines()
    if len(json_object) ==0:
        st.write('Please create new registry')
    else:
        with open('userdata.json', 'r') as openfile:
            json_object = json.load(openfile)
            name = json_object['name']
            email = json_object['email']
            base_currency = json_object['base_currency']
            target_currency = json_object['target_currency']
            st.title("Welcome {0}".format(name))
            st.write('Your email address is : {0}'.format(email))
            st.write('Your base currency is set to {0}'.format(base_currency))
            # r = get_exchange_rates("INR", ["USD", "EUR", "CAD"])
            # st.write(r)
            for i in target_currency:
                mini = list(i.values())
                print(mini)
                r,y = get_exchange_rates(base_currency,list(i.keys()))
                st.write('{0} -> min {1}, max {2}, current value {3}'.format(list(i.keys())[0],list(i.values())[0][0],list(i.values())[0][1], list(y.values())[0]))
        
else:
    st.write('Please create new registry')
        
        