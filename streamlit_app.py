import datetime
import pandas as pd
import streamlit as st
import openpyxl

st.set_page_config(
    page_title=" Trips & Visits",
    page_icon=":airplane:",
    layout="wide"
)

st.title(" ✈️ Trips & Visits Overview")
st.write("An overview of trips and visits for WY2024/2025")

df = openpyxl.load_workbook('namelist.xlsx')
sheet = df.active #Assuming the data is in the first sheet

# Page setup
update_page = st.Page(
    page = "view/update.py",
    title = "Update Details",
)

home_page = st.Page(
    page = "view/home.py",
    title = "Namelist",
    icon = "👤",
    default= True,
)

pg = st.navigation(pages=[update_page])
pg.run()