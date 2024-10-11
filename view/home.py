import datetime
import pandas as pd
import streamlit as st
import openpyxl
from streamlit_card import card

# Load the Excel dataset
df = pd.read_excel("namelist.xlsx")

# Create a search box
search_query = st.text_input("Search by Country or Company:")

# Filter the DataFrame based on the search query
if search_query:
    filtered_df = df[(df["Country"].str.contains(search_query, case=False)) | (df["Company"].str.contains(search_query, case=False))]
else:
    filtered_df = df

# Customize the card appearance
#st.markdown("<style>div.stCard {max-width: 300px;}</style>", unsafe_allow_html=True)

# Display the results in a card view
for index, row in filtered_df.iterrows():  
    st.markdown(f"""
        <div style="background-color: #f0f0f0; padding: 10px; border-radius: 10px; margin-bottom: 20px;">
            <div style="display: flex; justify-content: space-between;">
                <h4>{row["Name"]} ({row["Designation"]})</h4>
                <div style="padding: 5px; border-radius: 5px;">
                    <button style="background-color: green; color: white; padding: 5px; border: none; border-radius: 10px; cursor: pointer;">{row["Status"]}</button>
                </div>
            </div>
            <p>Country: {row["Country"]}</p>
            <p>Vehicle(s): {row["Vehicle"]}</p>
            <p>Company: {row["Company"]}</p>
            <p>Posting date: {row["Posting Date"]}</p>
            <p>Contact No.: {row["Contact No."]}</p>
            <p>Golf: {row["Golf"]}</p>
            <p>Golf handicap: {row["Golf Handicap"]}</p>
        </div>
    """, unsafe_allow_html=True)

    # Add JavaScript to set the background color dynamically
    st.markdown(f"""
        <script>
            var statusElement = document.getElementById('status_{index}');
            if (statusElement.textContent === 'Active') {{
                statusElement.style.backgroundColor = 'green';
                statusElement.style.color = 'white';
            }} else if (statusElement.textContent === 'Deposted') {{
                statusElement.style.backgroundColor = 'red';
                statusElement.style.color = 'white';
            }}
        </script>
    """, unsafe_allow_html=True)
