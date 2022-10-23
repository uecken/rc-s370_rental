import streamlit as st
import requests
import json

#endpoint= 'https://uo41eu.deta.dev'
endpoint= 'https://1hl0lg.deta.dev'

def app():
    st.title('もの登録')

    with st.form(key='object'):
        name:str = st.text_input('もの名称',max_chars=20)
        id_:str = st.text_input('ID',max_chars=30)
        register_place:str = st.text_input('登録場所','-',max_chars=15)
        data={
            'name':name,
            'id_':id_,
            'register_place':register_place,
        }
        submit_button = st.form_submit_button(label='登録')

        if submit_button:
            url=endpoint+ '/objects'
            res=requests.post(
                url,
                data=json.dumps(data)
            )

            if res.status_code== 200:
                st.success('もの登録完了')
