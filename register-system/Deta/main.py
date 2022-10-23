from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from deta import Deta
import json
from datetime import datetime as dt
from zoneinfo import ZoneInfo

# localの場合は、project keyが必要だが、Deta base上ではいらない
deta = Deta()
users = deta.Base("fastapi-users")
rooms = deta.Base("fastapi-rooms")
bookings = deta.Base("fastapi-bookings")
readers = deta.Base("fastapi-readers")
reads2 = deta.Base("fastapi-reads2")

app = FastAPI()

class User(BaseModel):
  name: str
  id_: str
  age: int
  hometown: str
  phone_number: str
  register_place: str

class Room(BaseModel):
  room_name: str
  capacity: int

class Booking(BaseModel):
  user_key: str
  room_key: str
  reserved_num: int
  start_date_time: str
  end_date_time: str

class Object(BaseModel):
  devide_id: str  #mac address
  card_id: str
  read_date: str

#どのReaderで誰が何をいつ使ったか分かるようにするため、
#まずReader MAC ID/object/設置場所の紐づけを行う
class Reader(BaseModel):
  reader_name: str
  reader_mac_id: str
  reader_place: str
  reader_and_objects: str

class Read2(BaseModel):
  object_id0: str
  object_id1: str
  object_id2: str
  reader_mac_id: str
  read_date: str

@app.get("/users")
def read_user():
  return next(users.fetch())

@app.post("/users",status_code=200)
def create_user(user: User):
  user= users.put(user.dict())
  return json.dumps(user)

@app.get("/rooms")
def read_room():
  return next(rooms.fetch())

@app.post("/rooms",status_code=200)
def create_room(room: Room):
  room= rooms.put(room.dict())
  return json.dumps(room)

@app.get("/bookings")
def read_booking():
  return next(bookings.fetch())

@app.post("/bookings",status_code=200)
def create_booking(booking: Booking):
  booking= bookings.put(booking.dict())
  return json.dumps(booking)

@app.get("/readers")
def read_reader():
  return next(readers.fetch())

@app.post("/readers",status_code=200)
def create_reader(reader: Reader):
  reader= readers.put(reader.dict())
  return json.dumps(reader)


@app.get("/reads")
def read_read():
  return next(reads2.fetch())

'''
@app.get("/reads/object_id/{object_id}")
async def read_object_id(object_id):
    return {"object_id":object_id}
'''

@app.post("/reads",status_code=200)
def create_read(read2: Read2):
  read2= reads2.put(read2.dict())
  return json.dumps(read2)

'''
@app.get("/read_regist/")
async def read_regist(object_id: str="default")
  read_regist_dict = {"object_id":object_id}
  return read_regist_dict
'''

'''
@app.get("/items2/{item_id}")
async def read_item(item_id: str, q: Union[str, None] = None, short: bool = False):
  item = {"item_id": item_id}
  if q:
    item.update({"q": q})
    if not short:
      item.update(
        {"description": "This is an amazing item that has a long description"}
      )
  return item

'''
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
  return fake_items_db[skip : skip + limit]


@app.get("/items2/")
async def read_item2(object_id: str):
  json = {"object_id":object_id}
  return json


@app.get("/items3/")
async def read_item3(object_id: str, mac_id:str):
  json = {"object_id":object_id, "mac_id":mac_id}
  return json


@app.get("/read_regist/")
async def read_regist(object_id0: str,object_id1: str,object_id2:str,reader_mac_id:str,read_date:str):
  tdatetime = dt.now(ZoneInfo("Asia/Tokyo"))
  tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
  json = {"object_id0":object_id0, "object_id1":object_id1, "object_id2":object_id2, "reader_mac_id":reader_mac_id, 'read_date':tstr}
  read2 = reads2.put(json)
  return json
