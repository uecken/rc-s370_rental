import streamlit as st
from multiapp import MultiApp
from apps import users, rooms, bookings, objects, readers, reads ,history
app=MultiApp()

app.add_app("users",users.app)
#app.add_app("rooms",rooms.app)
#app.add_app("bookings",bookings.app)
app.add_app("objects",objects.app)
app.add_app("readers",readers.app)
app.add_app("reads",reads.app)
app.add_app("history",history.app)

app.run()

