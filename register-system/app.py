import streamlit as st
from multiapp import MultiApp
from apps import users, rooms, bookings, objects, readers, reads ,history
app=MultiApp()

#app.add_app("rooms",rooms.app)
#app.add_app("bookings",bookings.app)
app.add_app("ものの読み取り一覧",reads.app)
app.add_app("もの登録",objects.app)
app.add_app("ユーザー登録",users.app)
app.add_app("リーダー登録",readers.app)
app.add_app("全履歴",history.app)

#app.add_app("rooms",rooms.app)
#app.add_app("bookings",bookings.app)

app.run()

