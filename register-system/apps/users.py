import streamlit as st
import requests
import json
import pandas as pd
import datetime
from zoneinfo import ZoneInfo

#endpoint= 'https://uo41eu.deta.dev'
endpoint= 'https://1hl0lg.deta.dev'

def app():
    st.title('ユーザー登録')

    tdatetime = datetime.datetime.now(ZoneInfo("Asia/Tokyo"))
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')

    with st.form(key='user'):
        name:str = st.text_input('ユーザー名',max_chars=20)
        id_:str = st.text_input('ID',max_chars=30)
        age:int = st.text_input('年齢','-',max_chars=3)
        hometown:str = st.text_input('出身','-',max_chars=15)
        register_place:str = st.text_input('登録場所','-',max_chars=15)
        #register_date:str = st.text_input('登録日','-',max_chars=15)
        phone_number:str = st.text_input('電話番号','-',max_chars=15)
        register_date:str = 1111
        data={
            'name':name,
            'id_':id_,
            'age':age,
            'hometown':hometown,
            'register_place':register_place,
            'register_date':tstr,
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


    # ユーザー一覧を取得
    url_reads= endpoint+ '/users'
    res_read= requests.get(url_reads)
    reads= res_read.json()

    reads_dict=[]
    for read in reads:
        read_dict= {}
        read_dict['name']= read['name']
        read_dict['id_']= read['id_']
        read_dict['register_place']= read['register_place']
        read_dict['register_date']= read['register_date']
        reads_dict.append(read_dict)

    read_list= pd.DataFrame(reads_dict)

    st.write('### ユーザー一覧')
    #st.table(read_list)
    st.dataframe(read_list,width=None,height=2000)

