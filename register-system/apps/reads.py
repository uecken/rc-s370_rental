import streamlit as st
import requests
import json
import pandas as pd
import datetime

endpoint= 'https://1hl0lg.deta.dev'

#いつ、誰のカードが、どのReaderで読まれたか分かれば良い

def app():
  st.title('読み取り履歴一覧')


  # 読み取り履歴を取得
  url_reads= endpoint+ '/reads'
  res_read= requests.get(url_reads)
  reads= res_read.json()

  reads_dict=[]
  for read in reads:
    read_dict= {}
    read_dict['reader_mac_id']= read['reader_mac_id']
    read_dict['object_id0']= read['object_id0']
    read_dict['object_id1']= read['object_id1']
    read_dict['object_id2']= read['object_id2']
    read_dict['read_date']= read['read_date']
    reads_dict.append(read_dict)

  read_list= pd.DataFrame(reads_dict)

  st.write('### 読み取り履歴一覧')
  #st.table(read_list)
  st.dataframe(read_list,width=None,height=2000)


'''
  reads_name= {}
  for read in reads :
    reads_name[read['name']]= read['key']
'''
