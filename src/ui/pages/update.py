import json
import streamlit as st
import os


def show_data(username, json_data):
    # json_data = json.loads(json_data)
    for datas in [json_data]:
      #   print("data",datas['name'])
        if datas["name"] == username:
            return datas
        

st.title("This is PageTwo Geeks.") 
st.sidebar.success("You are currently viewing Page Two Geek")

if ('userdata.json' in os.listdir()):
    with open('userdata.json', 'r') as openfile:
       json_object = openfile.readlines()
    if len(json_object) ==0:
        st.write('Please create new registry')
    else:
        openfile.close()
        with open('userdata.json', 'r') as openfile:
            json_object = json.load(openfile)
        print(json_object)
        name = json_object['name']
        email = json_object['email']
        base_currency = st.selectbox('base currency',['INR','USD','CAD'],index=['INR','USD','CAD'].index(json_object['base_currency']))
        # key = [curr.keys() for curr in json_object['target_currency']]
        traget_currency = st.multiselect('target currency',['INR','CAD','USD','YEN'],default=[list(curr.keys())[0] for curr in json_object['target_currency']])
        lst = []

        for i in range(len(traget_currency)):
            number_min = st.number_input(traget_currency[i],key=str(traget_currency[i])+"_min")
            number_max = st.number_input(traget_currency[i],key=str(traget_currency[i])+"_max")
            lst.append({traget_currency[i] : [number_min,number_max]})
    
        with st.form('tar'):
            st.write(lst)
            submit = st.form_submit_button('Submit')
        if submit:
            openfile.close()
            dct = {
                       'name' : name,
                       'email': email,
                       'base_currency': base_currency,
                       'target_currency': lst,
                }
            json_object = json.dumps(dct, indent=4)
            # print(type(json_object))
            with open("userdata.json", "w") as outfile: 
               outfile.write(json_object)
            with open('userdata.json', 'r') as openfile:
               json_object = json.load(openfile)
            show_data(name, json_object)
else:
    st.write("Create new registery")
            