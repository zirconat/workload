import datetime
import pandas as pd
import streamlit as st
import openpyxl

# Load the Excel dataset
df = pd.read_excel("namelist.xlsx")

# Create a search box
search_query = st.text_input("Search by name or country:")

# Filter the DataFrame based on the search query
if search_query:
    filtered_df = df[(df["Name"].str.contains(search_query, case=False)) | (df["Country"].str.contains(search_query, case=False))]
else:
    filtered_df = df

# Display the results in a card view
for index, row in filtered_df.iterrows():
    st.card(f"""
        **Name:** {row["Name"]}
        **Country:** {row["Country"]}
        **Other information:** {row["Other information"]}
    """)