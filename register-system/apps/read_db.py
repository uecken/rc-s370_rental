


import datetime
from deta import Deta  # Import Deta
import json

# Initialize with a Project Key
deta = Deta("d02hi2dq_nDB1zRBdCDNpMP3NnhuRKuCHFxJAfpSJ")

# This how to connect to or create a database.
db = deta.Base("fastapi-reads2")



res = db.fetch({"read_date?gt":"2022-11-04 05:49:18"},limit=5)
#res = db.fetch({"query":[{"read_date?gt":"2022-11-04 05:49:18"}],"limit":10,"last":""})
items = res.items
print(items)

items_dict = json.dumps(items,indent=2,ensure_ascii=False)
print(items_dict)

sorted_res = sorted(items_dict,key=lambda s: s[4])
print(sorted_res)
