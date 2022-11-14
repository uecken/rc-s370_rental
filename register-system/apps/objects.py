import streamlit as st
import requests
import json
import pandas as pd
import datetime
from deta import Deta  # Import Deta
from zoneinfo import ZoneInfo
import time

#endpoint= 'https://uo41eu.deta.dev'
endpoint= 'https://1hl0lg.deta.dev'

deta = Deta("d02hi2dq_nDB1zRBdCDNpMP3NnhuRKuCHFxJAfpSJ")
db = deta.Base("fastapi-reads2")
read_obj=""
read_id="-"
reads_obj_pd=""

#reads_obj_pd = pd.DataFrame({'a':[1,2]})


def clear_text():
  #read_object_list()
  st.session_state["ID"] = read_object_list()
  st.session_state["NAME"] = ""
  st.session_state["PLACE"] = ""
    

def app():
  #read_object_list()
  
  st.title('もの登録')
  #time.sleep(1)

  #generate_form()
  

  #read_object_list()
  time.sleep(0.5)

  '''
  form = st.form("object2")
  name:str = form.text_input('もの名称',max_chars=20)
  id_:str = form.text_input('ID',read_id,max_chars=30,key="ID")
  register_place:str = form.text_input('登録場所','-',max_chars=15)
  
  data={
       'name':name,
        'id_':id_,
        'register_place':register_place
  }
  

  submit_button = form.form_submit_button("Submit")
  if submit_button:
    url=endpoint+ '/objects2'
    res=requests.post(
      url,
      data=json.dumps(data)
    )
  '''

  '''
  if st.button(label='再読み込み'):
    st.experimental_rerun()
    form.text_input("ID", "", key="2")
    #form.text_input('ID',read_id,max_chars=30)
  '''
  #st.button("clear text input", on_click=clear_text)
  
  with st.form(key='object2'):
    name:str = st.text_input('もの名称',max_chars=20,key="NAME")
    id_:str = st.text_input('ID',read_id,max_chars=30,key="ID")
    register_place:str = st.text_input('登録場所','-',max_chars=15,key="PLACE")
    data={
         'name':name,
          'id_':id_,
          'register_place':register_place
    }
    clear = st.form_submit_button(label="ID反映",on_click=clear_text)
    submit_button = st.form_submit_button(label='もの登録')

    if submit_button:
      url=endpoint+ '/objects2'
      res=requests.post(
        url,
        data=json.dumps(data)
      )
 

  '''
  if st.button(label='Update List!'):
    read_object_list()
  '''

  # ==読取一覧を表示
  st.write('### 最新の読み取り一覧')
  read_object_list()
    #read_object_list()
  try:
    st.dataframe(reads_obj_pd,width=None,height=200)
  except:
    st.write('(30分以内の最新5件を反映します)')
    pass

  # ==モノ一覧を取得
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


def read_object_list():  
  tdatetime = datetime.datetime.now(ZoneInfo("Asia/Tokyo"))
  query_date = tdatetime - datetime.timedelta(minutes=10)
  query_tstr = query_date.strftime('%Y-%m-%d %H:%M:%S')
  #st.write(query_date)
  query = {"read_date?gt":str(query_tstr)}
  reads_obj = db.fetch(query,limit=10).items

  global reads_obj_pd
  try:
    reads_obj_pd = pd.DataFrame(reads_obj).sort_values('read_date',ascending=False)
    read_id = reads_obj_pd.iloc[0]["object_id0"]
    #st.dataframe(reads_obj_pd,width=None,height=200)
  except KeyError as e:
    st.write("最新の読み取りはありません")
    return
  #print(reads_obj_pd)
  #global read_id
  #st.write(read_id)
  #st.table(reads_obj_pd)
  #st.dataframe(reads_obj_pd,width=None,height=200)
  return read_id


def generate_form():
  global read_id
  read_object_list()
  time.sleep(0.5)
  with st.form(key='object2'):
    name:str = st.text_input('もの名称',max_chars=20)
    id_:str = st.text_input('ID',read_id,max_chars=30)
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

