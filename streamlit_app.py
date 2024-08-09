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

def main():
    df = pd.read_excel("namelist.xlsx")

    # Function to display dataframe
    def display_data():
        st.dataframe(df)

    # Function to add a new record
    def add_record():
        with st.form("add_form"):
            # Generate new S/N
            new_sn = df['S/N'].max() + 1

            country = st.text_input("Country")
            company = st.text_input("Company")
            name = st.text_input("Name")
            designation = st.text_input("Designation")
            diet = st.text_input("Dietary Restrictions")
            contact = st.text_input("Contact No.")
            address = st.text_input("Address")
            vehicle = st.text_input("Vehicle")
            golf = st.selectbox("Golf", ["Yes", "No"])
            handicap = st.text_input("Golf Handicap (if not applicable, key in 'N.A.')")
            posting_date = st.date_input("Posting Date")
            deposted_date = st.date_input("(Expected) Deposted Date")
            status = st.selectbox("Status", ["Active", "Deposted"])

            submitted = st.form_submit_button("Add")

            if submitted:
                new_record = {
                    "S/N": new_sn,
                    "Country": country,
                    "Company": company,
                    "Name": name,
                    "Designation": designation,
                    "Dietary Restrictions": diet,
                    "Contact No.": contact,
                    "Address": address,
                    "Vehicle": vehicle,
                    "Golf": golf,
                    "Golf Handicap": handicap,
                    "Posting Date": posting_date,
                    "Deposted Date": deposted_date,
                    "Status": status
                }
                df = pd.concat([df, pd.Dataframe([new_record])], ignore_index=True)
                display_data()

    # Function to edit existing record
    def edit_record():
        sn = st.text_input("Enter the S/N of the record to edit")

        if sn in df['S/N'].values:
            with st.form("edit_form"):
                # Find the index of the record to edit
                index = df[df['S/N'] == sn].index[0]
                country = st.text_input("Country", value=df.at[index, "Country"])
                company = st.text_input("Company", value=df.at[index, "Company"])
                name = st.text_input("Name", value=df.at[index, "Name"])
                designation = st.text_input("Designation", value=df.at[index, "Designation"])
                dietary_restrictions = st.text_input("Dietary Restrictions", value=df.at[index, "Dietary Restrictions"])
                contact_no = st.text_input("Contact No.", value=df.at[index, "Contact No."])
                address = st.text_input("Address", value=df.at[index, "Address"])
                vehicle = st.text_input("Vehicle", value=df.at[index, "Vehicle"])
                golf = st.selectbox("Golf", ["Yes", "No"], index=["Yes" if df.at[index, "Golf"] == "Yes" else "No"])
                golf_handicap = st.text_input("Golf Handicap", value=df.at[index, "Golf Handicap"])
                posting_date = st.date_input("Posting Date", value=pd.to_datetime(df.at[index, "Posting Date"]))
                deposted_date = st.date_input("Deposted Date", value=pd.to_datetime(df.at[index, "Deposted Date"]))
                status = st.selectbox("Status", ["Active", "Deposted"], index=["Active" if df.at[index, "Status"] == "Active" else "Deposted"])

                submitted = st.form_submit_button("Update")

                if submitted:
                    df.at[index, "S/N"] = sn
                    df.at[index, "Country"] = country
                    df.at[index, "Company"] = company
                    df.at[index, "Name"] = name
                    df.at[index, "Designation"] = designation
                    df.at[index, "Dietary Restrictions"] = dietary_restrictions
                    df.at[index, "Contact No."] = contact_no
                    df.at[index, "Address"] = address
                    df.at[index, "Vehicle"] = vehicle
                    df.at[index, "Golf"] = golf
                    df.at[index, "Golf Handicap"] = golf_handicap
                    df.at[index, "Posting Date"] = posting_date
                    df.at[index, "Deposted Date"] = deposted_date
                    df.at[index, "Status"] = status
                    display_data()

    # Function to delete a record
    def delete_record():
        sn = st.text_input("Enter the S/N of the record to delete")

        if sn in df['S/N'].values:
            df = df[df['S/N'] != sn]
            display_data()
    
    # Main UI
    display_data()

    st.button("Add New", on_click=add_record)
    st.button("Update", on_click=edit_record)
    st.button("Delete", on_click=delete_record)

if __name__ == "__main__":
    main()