import streamlit as st
import requests
import json
import pandas as pd
import datetime
from zoneinfo import ZoneInfo

#endpoint= 'https://uo41eu.deta.dev'
endpoint= 'https://1hl0lg.deta.dev'

def app():
    st.title('リーダー登録')

    tdatetime = datetime.datetime.now(ZoneInfo("Asia/Tokyo"))
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')


    with st.form(key='reader'):
        reader_name:str = st.text_input('リーダー名称',max_chars=20)
        reader_mac_id:str = st.text_input('MAC-ID',max_chars=30)
        reader_place:str = st.text_input('設置場所','-',max_chars=15)
        reader_and_objects:str = st.text_input('読み取り時の利用機器','-',max_chars=15)
        data={
            'reader_name':reader_name,
            'reader_mac_id':reader_mac_id,
            'reader_place':reader_place,
            'reader_and_objects':reader_and_objects,
            'register_date':tstr
        }
        submit_button = st.form_submit_button(label='登録')

        if submit_button:
            url=endpoint+ '/readers'
            res=requests.post(
                url,
                data=json.dumps(data)
            )

            if res.status_code== 200:
                st.success('リーダー登録完了')


    # 読み取り履歴を取得
    url_readers= endpoint+ '/readers'
    res_reader= requests.get(url_readers)
    readers= res_reader.json()
    
    reads_dict=[]
    for read in readers:
        read_dict= {}
        read_dict['reader_name']= read['reader_name']
        read_dict['reader_mac_id']= read['reader_mac_id']
        read_dict['reader_place']= read['reader_place']
        read_dict['reader_and_objects']= read['reader_and_objects']
        read_dict['register_date']= read['register_date']
        reads_dict.append(read_dict)

    read_list= pd.DataFrame(reads_dict).sort_values('register_date',ascending=True)

    st.write('### リーダー一覧')
    #st.table(read_list)
    st.dataframe(read_list,width=None,height=2000)

