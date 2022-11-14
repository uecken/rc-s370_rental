import streamlit as st
import requests
import json
import pandas as pd
import datetime
from deta import Deta  # Import Deta
from zoneinfo import ZoneInfo

#endpoint= 'https://1hl0lg.deta.dev'

#WebAPI経由だと日付ソートして取得が難しいため
#Databaseへ直接接続するように変更
deta = Deta("d02hi2dq_nDB1zRBdCDNpMP3NnhuRKuCHFxJAfpSJ")
db = deta.Base("fastapi-reads2")


#いつquery2 ={"query": [{"read_date?gt": "2022-11-04 05:49:18"}],"limit": 3}、誰のカードが、どのReaderで読まれたか分かれば良い

def app():
  st.title('読み取り履歴一覧')


  # 読み取り履歴を取得
  '''
  url_reads= endpoint+ '/reads'
  res_read= requests.get(url_reads)
  reads= res_read.json()
  '''

  tdatetime = datetime.datetime.now(ZoneInfo("Asia/Tokyo"))
  tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
  query_date = tdatetime - datetime.timedelta(days=15)
  query_tstr = query_date.strftime('%Y-%m-%d %H:%M:%S')
  st.write(query_date)
  query = {"read_date?gt":str(query_tstr)}

  reads = db.fetch(query,limit=50).items
  #reads = db.fetch({"read_date?gt":"2022-11-04 05:49:18"},limit=5).items
  #reads = db.fetch({"read_date?gt":},limit=5).items
  #reads = json.dumps(res,indent=2,ensure_ascii=False)
  #reads = sorted(reads,key=lambda s: s[4])
  #st.table(reads)
  

  '''
  reads_dict=[]
  for read in reads:
    read_dict= {}
    read_dict['reader_mac_id']= read['reader_mac_id']
    read_dict['object_id0']= read['object_id0']
    read_dict['object_id1']= read['object_id1']
    read_dict['object_id2']= read['object_id2']
    read_dict['read_date']= read['read_date']
    reads_dict.append(read_dict)
  '''

  try:
    read_pd= pd.DataFrame(reads).sort_values('read_date',ascending=False)
    print(read_pd)
    st.write('### 読み取り履歴一覧')
    st.write('15日以内')
    #st.table(read_list)
    st.dataframe(read_pd,width=None,height=2000)
  except Exception:
    st.write('15日以内の読み取り無し')
  

'''
https://1hl0lg.deta.dev  reads_name= {}
  for read in reads :
    reads_name[read['name']]= read['key']
'''

