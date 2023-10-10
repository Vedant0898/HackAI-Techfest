import os
import json

import streamlit as st

from utils.api_utils import get_exchange_rates

st.set_page_config(page_title="pip.ai")

if "data.json" in os.listdir():
    # Check for data.json file and load data if present
    with open("data.json", "r") as openfile:
        json_object = openfile.readlines()
    if len(json_object) == 0:
        # If file is empty ask user to create new preference
        st.write("Please create new user preference")
    else:
        # Else display user preference and ask user to update if required
        with open("data.json", "r") as openfile:
            json_object = json.load(openfile)
            name = json_object["name"]
            email = json_object["email"]
            base_currency = json_object["base_currency"]
            target_currency = json_object["target_currency"]
            st.title("Welcome {0}".format(name))
            st.write("Your email address is : {0}".format(email))
            st.write("Your base currency is set to {0}".format(base_currency))

            for i in target_currency:
                mini = list(i.values())
                # call api to get current exchange rates and display
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
    # Else ask user to create new preference
    st.write("Please create new preference")
