import json
import streamlit as st
import os
import pickle

file = open("currencies.pkl", "rb")
currencies = pickle.load(file)


def show_data(username, json_data):
    # json_data = json.loads(json_data)
    for datas in [json_data]:
        #   print("data",datas['name'])
        if datas["name"] == username:
            return datas


st.title("This is PageTwo Geeks.")
st.sidebar.success("You are currently viewing Page Two Geek")

if "data.json" in os.listdir():
    with open("data.json", "r") as openfile:
        json_object = openfile.readlines()
    if len(json_object) == 0:
        st.write("Please create new registry")
    else:
        openfile.close()
        with open("data.json", "r") as openfile:
            json_object = json.load(openfile)
        print(json_object)
        name = json_object["name"]
        email = json_object["email"]
        base_currency = st.selectbox(
            "base currency",
            currencies,
            index=currencies.index(json_object["base_currency"]),
        )
        # key = [curr.keys() for curr in json_object['target_currency']]
        traget_currency = st.multiselect(
            "target currency",
            currencies,
            default=[list(curr.keys())[0] for curr in json_object["target_currency"]],
        )
        lst = []

        for i in range(len(traget_currency)):
            number_min = st.number_input(
                str(traget_currency[i]) + " mix",
                key=str(traget_currency[i]) + "_min",
                value=0.0000001,
                format="%.5f",
            )
            number_max = st.number_input(
                str(traget_currency[i]) + " max",
                key=str(traget_currency[i]) + "_max",
                value=0.0000001,
                format="%.5f",
            )
            lst.append({traget_currency[i]: [number_min, number_max]})

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
            # print(type(json_object))
            with open("data.json", "w") as outfile:
                outfile.write(json_object)
            with open("data.json", "r") as openfile:
                json_object = json.load(openfile)
            show_data(name, json_object)
else:
    st.write("Create new registery")
