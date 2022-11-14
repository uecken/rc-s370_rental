import streamlit as st
import requests
import json
import pandas as pd

#endpoint= 'https://uo41eu.deta.dev'
endpoint= 'https://1hl0lg.deta.dev'

def app():
    st.title('全履歴')

    # ユーザー一覧を取得
    url_users= endpoint+ '/users'
    res_user= requests.get(url_users)
    users= res_user.json()
    users_dict=[]
    for user in users:
        user_dict= {}
        user_dict['name']= user['name']
        user_dict['id_']= user['id_']
        user_dict['register_place']= user['register_place']
        user_dict['register_date']= user['register_date']
        users_dict.append(user_dict)

    user_list= pd.DataFrame(users_dict)
    st.write("### ユーザー一覧")
    st.dataframe(user_list,width=None,height=200)

    # もの一覧を取得
    url_objects= endpoint+ '/objects2'
    res_object= requests.get(url_objects)
    objects= res_object.json()
    objects_dict=[]
    for object_one in objects:
        object_dict= {}
        object_dict['name']= object_one['name']
        object_dict['id_']= object_one['id_']
        object_dict['register_place']= object_one['register_place']
        objects_dict.append(object_dict)

    object_list= pd.DataFrame(objects_dict)
    st.write("### 登録もの一覧")
    st.dataframe(object_list,width=None,height=200)

    # リーダー一覧を取得
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
        reads_dict.append(read_dict)

    reader_list= pd.DataFrame(reads_dict)
    st.write("### リーダー一覧")
    st.dataframe(reader_list,width=None,height=200)


    # 読み取り一覧と読み取り機器を取得
    url_reads= endpoint+ '/reads'
    res_reads= requests.get(url_reads)
    reads= res_reads.json()

    reads_dict=[]
    for read in reads:
        try:
          read_dict= {}
          read_dict['reader_mac_id']= read['reader_mac_id']
          read_dict['id_']= read['object_id0']
          read_dict['object_id1']= read['object_id1']
          read_dict['object_id2']= read['object_id2']
          read_dict['read_date']= read['read_date']
          reads_dict.append(read_dict)
        except:
          st.write('pass')

    read_list= pd.DataFrame(reads_dict)

    #df = pd.read_json(reads,orient='index')
    #df = pd.read_json(reads).transpose()
    #df = pd.DataFrame.from_dict(reads, orient='index').T

    #st.dataframe(df,width=None,height=2000)
    st.write("### 読み取り一覧")
    st.dataframe(read_list,width=None,height=300)

    #read_list= pd.read_json(reads,orient='index')
    #st.write('### ユーザー一覧')

    st.write("### 読み取り一覧と読み取り機器")
    merged_user_read = pd.merge(user_list,read_list,how = 'inner',on='id_')
    merged_user_read_reader = pd.merge(merged_user_read,reader_list,how = 'inner',on='reader_mac_id')
    st.dataframe(merged_user_read_reader,width=None,height=500)

