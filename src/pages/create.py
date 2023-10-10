import streamlit as st
import json
from streamlit import session_state as ss
import pickle
import os

file = open("currencies.pkl", "rb")
currencies = pickle.load(file)


def show_data(username, json_data):
    #  json_data = json.load(json_data)
    for datas in [json_data]:
        #   print("data",datas['name'])
        if datas["name"] == username:
            return datas


def create_file():
    file1 = open("data.json", "a")  # append mode
    file1.close()


def check_value(data, val):
    return any(player["email"] == val for player in len(data))


st.title("This is PageOne Geeks.")
st.sidebar.success("You are currently viewing Page One Geek")


def create_form():
    # with open('data.json', 'r') as openfile:
    #        json_object = json.load(openfile)
    username = st.text_input("Name", key="name")
    email = st.text_input("Email", key="email")
    base_currency = st.selectbox("base currency", currencies)
    traget_currency = st.multiselect("target currency", currencies)
    lst = []

    for i in range(len(traget_currency)):
        number_min = st.number_input(
            str(traget_currency[i]) + " min",
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

    with st.form("tar", clear_on_submit=True):
        st.write(lst)
        submit = st.form_submit_button("Submit")
    if submit:
        dct = {
            "name": username,
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
        ss["show_form"] = False


if "data.json" in os.listdir():
    with open("data.json", "r") as openfile:
        json_object = openfile.readlines()
    if len(json_object) == 0:
        # newScenario = st.button("Create New Scenario", key="a")

        create_form()
    else:
        with open("data.json", "r") as openfile:
            json_object = json.load(openfile)
        st.write(show_data(json_object["name"], json_object))


else:
    create_file()

    name_in_dct = False
    newScenario = st.button("Create New Scenario", key="a")

    if "show_form" not in ss:
        ss["show_form"] = False
    if newScenario:
        ss["show_form"] = True

    if not ss["show_form"]:
        create_form()
