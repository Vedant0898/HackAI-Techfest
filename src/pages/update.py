import os
import json
import pickle

import streamlit as st

st.set_page_config(page_title="pip.ai")

file = open("currencies.pkl", "rb")
CURRENCIES = pickle.load(file)


def show_data(username, json_data):
    for datas in [json_data]:
        if datas["name"] == username:
            return datas


if "data.json" in os.listdir():
    # Check for data.json file and load data if present
    with open("data.json", "r") as openfile:
        json_object = openfile.readlines()
    if len(json_object) == 0:
        st.write("Please create new user preference")
    else:
        st.title("Update the data")
        openfile.close()
        with open("data.json", "r") as openfile:
            json_object = json.load(openfile)
        name = json_object["name"]
        email = json_object["email"]
        base_currency = st.selectbox(
            "base currency",
            CURRENCIES,
            index=CURRENCIES.index(json_object["base_currency"]),
        )
        target_currency = st.multiselect(
            "target currency",
            CURRENCIES,
            default=[list(curr.keys())[0] for curr in json_object["target_currency"]],
        )
        lst = []
        tmp = json_object["target_currency"]
        d = {}
        for i in tmp:
            d.update(i)

        for i in range(len(target_currency)):
            val = [0.0, 0.0]
            if target_currency[i] in d.keys():
                val = d[target_currency[i]]

            number_min = st.number_input(
                str(target_currency[i]) + " min",
                key=str(target_currency[i]) + "_min",
                value=val[0],
                format="%.5f",
            )
            number_max = st.number_input(
                str(target_currency[i]) + " max",
                key=str(target_currency[i]) + "_max",
                value=val[1],
                format="%.5f",
            )
            lst.append({target_currency[i]: [number_min, number_max]})

        with st.form("tar"):
            st.write(lst)
            submit = st.form_submit_button("Submit")
        if submit:
            openfile.close()
            dct = {
                "name": name,
                "email": email,
                "hasChanged": True,
                "base_currency": base_currency,
                "target_currency": lst,
            }
            json_object = json.dumps(dct, indent=4)
            with open("data.json", "w") as outfile:
                outfile.write(json_object)
            with open("data.json", "r") as openfile:
                json_object = json.load(openfile)
            show_data(name, json_object)
else:
    # Else ask user to create new preference
    st.write("Create new user preference")
