import datetime
import pandas as pd
import streamlit as st
import openpyxl

# Show app title and description.
st.set_page_config(
    page_title="Namelist", 
    page_icon="👤",
    layout= "wide",
)
st.title("👤 Namelist")

df = pd.read_excel("namelist.xlsx")

# Save the dataframe in session state (a dictionary-like object that persists across
# page runs). This ensures our data is persisted when the app updates.
st.session_state.df = df

st.dataframe(df)