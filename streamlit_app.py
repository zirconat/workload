import datetime
import pandas as pd
import streamlit as st
import openpyxl

st.set_page_config(
    page_title=" Trips & Visits",
    page_icon=":airplane:",
    layout="wide"
)

st.title(" Database")
st.write("Find the one you need!")

df = openpyxl.load_workbook('namelist.xlsx')
sheet = df.active #Assuming the data is in the first sheet

# Page setup
home_page = st.Page(
    page = "view/home.py",
    title = "Home",
    icon = "🏠",
    default= True,
)

update_page = st.Page(
    page = "view/update.py",
    title = "Update Details",
    icon = "✍🏼"
)

pg = st.navigation(pages=[home_page, update_page])
pg.run()