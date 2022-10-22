import streamlit as st
from multiapp import MultiApp
from apps import home, data_stats

app = MultiApp() 

app.add_app("Home", home.app)
app.add_app("Data Stats", data_stats.app) 

app.run()
