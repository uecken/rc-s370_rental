import streamlit as st
import requests
import json

#endpoint= 'https://uo41eu.deta.dev'
endpoint= 'https://1hl0lg.deta.dev'

def app():
    st.title('ユーザー登録')

    with st.form(key='user'):
        name:str = st.text_input('ユーザー名',max_chars=20)
        id_:str = st.text_input('ID',max_chars=30)
        age:int = st.text_input('年齢','-',max_chars=3)
        hometown:str = st.text_input('出身','-',max_chars=15)
        register_place:str = st.text_input('登録場所','-',max_chars=15)
        phone_number:str = st.text_input('電話番号','-',max_chars=15)
        data={
            'name':name,
            'id_':id_,
            'age':age,
            'hometown':hometown,
            'register_place':register_place,
            'phone_number':phone_number
        }
        submit_button = st.form_submit_button(label='登録')

        if submit_button:
            url=endpoint+ '/users'
            res=requests.post(
                url,
                data=json.dumps(data)
            )

            if res.status_code== 200:
                st.success('ユーザー登録完了')
