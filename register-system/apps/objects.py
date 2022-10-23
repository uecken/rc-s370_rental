import streamlit as st
import requests
import json
import pandas as pd

#endpoint= 'https://uo41eu.deta.dev'
endpoint= 'https://1hl0lg.deta.dev'

def app():
    st.title('もの登録')

    with st.form(key='object2'):
        name:str = st.text_input('もの名称',max_chars=20)
        id_:str = st.text_input('ID',max_chars=30)
        register_place:str = st.text_input('登録場所','-',max_chars=15)
        data={
            'name':name,
            'id_':id_,
            'register_place':register_place
        }
        submit_button = st.form_submit_button(label='登録')

        if submit_button:
            url=endpoint+ '/objects2'
            res=requests.post(
                url,
                data=json.dumps(data)
            )

            if res.status_code== 200:
                st.success('もの登録完了')


    # モノ一覧を取得
    url_reads= endpoint+ '/objects2'
    res_read= requests.get(url_reads)
    reads= res_read.json()

    reads_dict=[]
    for read in reads:
        read_dict= {}
        read_dict['name']= read['name']
        read_dict['id_']= read['id_']
        read_dict['register_place']= read['register_place']
        reads_dict.append(read_dict)

    read_list= pd.DataFrame(reads_dict)

    st.write('### 登録もの一覧')
    #st.table(read_list)
    st.dataframe(read_list,width=None,height=2000)
