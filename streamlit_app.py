import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image
import io

# --- MUST BE THE FIRST STREAMLIT COMMAND ---
st.set_page_config(layout="wide", page_title="Contact Card App 📞")

# --- Custom CSS for Rounded Images and Card Styling ---
st.markdown(
    """
    <style>
    .profile-pic-container img {
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid #ddd; /* Optional: add a subtle border */
    }
    .contact-card {
        background-color: #333; /* Darker background for the card */
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        color: #f0f2f6; /* Light text color */
    }
    .contact-card h3 {
        color: #f0f2f6;
        margin-top: 0;
        margin-bottom: 5px;
    }
    .contact-card p {
        margin-bottom: 2px;
        font-size: 14px;
    }
    .tier-badge {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 5px;
        font-weight: bold;
        color: white;
        margin-left: 10px;
    }
    .tier-A { background-color: #007bff; } /* Blue */
    .tier-B { background-color: #28a745; } /* Green */
    .tier-C { background-color: #ffc107; color: #333;} /* Yellow */
    .tier-Untiered { background-color: #6c757d; } /* Gray */

    .status-badge {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 5px;
        font-weight: bold;
        color: white;
        margin-left: 10px;
    }
    .status-Active { background-color: #28a745; } /* Green */
    .status-Inactive { background-color: #dc3545; } /* Red */

    /* Removed .info-grid as we're using st.columns directly now */
    .info-item {
        margin-bottom: 5px;
    }
    .stButton > button {
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- 0. Data Initialization and Session State Management ---
if 'contacts_df' not in st.session_state:
    st.session_state.contacts_df = pd.DataFrame(
        columns=[
            "Name", "Designation", "Country", "Company", "Phone Number",
            "Office Number", "Office Address", "Home Address", "Hobbies",
            "Dietary Restrictions", "Celebrated Festivities",
            "Events Invited To", "Status", "Tiering", "Profile Picture",
            "Last Updated By", "Last Updated On", "History"
        ]
    )
    # Add some dummy data for demonstration
    st.session_state.contacts_df.loc[0] = [
        "Albert", "SC, Abc", "Australia", "CompanyA",
        "98765432", "N/A", "123 bsdlk slhf", "456 Home Rd, Perth",
        "sleeping", "NIL", "Deepavali", "NYR, ALSE",
        "Active", "A", None, # No profile picture for Albert initially
        "System", datetime.now().strftime("%d %b %y, %I:%M %p"), []
    ]
    st.session_state.contacts_df.loc[1] = [
        "Bob The Builder", "Project Manager", "Canada", "BuildCo",
        "987-654-3210", "654-321-0987", "789 Construction Blvd, Toronto",
        "101 Maple Lane, Toronto", "Gardening, Cycling", "None", # No profile picture for Bob initially
        "Canada Day", "Client Meeting", "Active", "B", None,
        "System", datetime.now().strftime("%d %b %y, %I:%M %p"), []
    ]
    st.session_state.contacts_df.loc[2] = [
        "Charlie Chaplin", "Actor", "UK", "Comedy Gold Studios",
        "555-123-4567", "555-987-6543", "Studio 5, London",
        "1 Baker Street, London", "Filmmaking, Chess", "Vegan",
        "Halloween", "Film Premiere", "Inactive", "C", None, # No profile picture for Charlie initially
        "System", datetime.now().strftime("%d %b %y, %I:%M %p"), []
    ]

if 'user_role' not in st.session_state:
    st.session_state.user_role = None

if 'show_add_form' not in st.session_state:
    st.session_state.show_add_form = False

# New session state for in-card editing
if 'editing_contact_index' not in st.session_state:
    st.session_state.editing_contact_index = None # Stores the index of the contact being edited

# --- 1. User Authentication ---
def login():
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        if username == "admin" and password == "adminpass":
            st.session_state.user_role = "admin"
            st.sidebar.success("Logged in as Admin!")
            st.rerun()
        elif username == "user" and password == "userpass":
            st.session_state.user_role = "user"
            st.sidebar.success("Logged in as User!")
            st.rerun()
        else:
            st.sidebar.error("Invalid username or password")

def logout():
    if st.sidebar.button("Logout"):
        st.session_state.user_role = None
        # Re-initialize contacts_df to its original state (dummy data)
        st.session_state.contacts_df = pd.DataFrame(
            columns=[
                "Name", "Designation", "Country", "Company", "Phone Number",
                "Office Number", "Office Address", "Home Address", "Hobbies",
                "Dietary Restrictions", "Celebrated Festivities",
                "Events Invited To", "Status", "Tiering", "Profile Picture",
                "Last Updated By", "Last Updated On", "History"
            ]
        )
        st.session_state.contacts_df.loc[0] = [
            "Albert", "SC, Abc", "Australia", "CompanyA",
            "98765432", "N/A", "123 bsdlk slhf", "456 Home Rd, Perth",
            "sleeping", "NIL", "Deepavali", "NYR, ALSE",
            "Active", "A", None,
            "System", datetime.now().strftime("%d %b %y, %I:%M %p"), []
        ]
        st.session_state.contacts_df.loc[1] = [
            "Bob The Builder", "Project Manager", "Canada", "BuildCo",
            "987-654-3210", "654-321-0987", "789 Construction Blvd, Toronto",
            "101 Maple Lane, Toronto", "Gardening, Cycling", "None",
            "Canada Day", "Client Meeting", "Active", "B", None,
            "System", datetime.now().strftime("%d %b %y, %I:%M %p"), []
        ]
        st.session_state.contacts_df.loc[2] = [
            "Charlie Chaplin", "Actor", "UK", "Comedy Gold Studios",
            "555-123-4567", "555-987-6543", "Studio 5, London",
            "1 Baker Street, London", "Filmmaking, Chess", "Vegan",
            "Halloween", "Film Premiere", "Inactive", "C", None,
            "System", datetime.now().strftime("%d %b %y, %I:%M %p"), []
        ]
        st.rerun()

# --- 2. Contact Card Display and Editing ---
def edit_contact_form(contact, index):
    st.markdown("<h4>Edit Contact</h4>", unsafe_allow_html=True)
    with st.form(key=f"edit_form_{index}"):
        # Pre-fill with current contact data
        name = st.text_input("Name*", value=contact["Name"], key=f"edit_name_{index}")
        designation = st.text_input("Designation*", value=contact["Designation"], key=f"edit_designation_{index}")
        country = st.text_input("Country*", value=contact["Country"], key=f"edit_country_{index}")
        company = st.text_input("Company*", value=contact["Company"], key=f"edit_company_{index}")
        phone_number = st.text_input("Phone Number", value=contact["Phone Number"], key=f"edit_phone_number_{index}")
        office_number = st.text_input("Office Number", value=contact["Office Number"], key=f"edit_office_number_{index}")
        office_address = st.text_area("Office Address", value=contact["Office Address"], key=f"edit_office_address_{index}")
        home_address = st.text_area("Home Address", value=contact["Home Address"], key=f"edit_home_address_{index}")
        hobbies = st.text_input("Hobbies", value=contact["Hobbies"], key=f"edit_hobbies_{index}")
        dietary_restrictions = st.text_input("Dietary Restrictions", value=contact["Dietary Restrictions"], key=f"edit_dietary_restrictions_{index}")
        celebrated_festivities = st.text_input("Celebrated Festivities", value=contact["Celebrated Festivities"], key=f"edit_celebrated_festivities_{index}")
        events_invited_to = st.text_input("Events Invited To", value=contact["Events Invited To"], key=f"edit_events_invited_to_{index}")
        status = st.selectbox("Status", ["Active", "Inactive"], index=["Active", "Inactive"].index(contact["Status"]), key=f"edit_status_{index}")
        tiering = st.selectbox("Tiering", ["A", "B", "C", "Untiered"], index=["A", "B", "C", "Untiered"].index(contact["Tiering"]), key=f"edit_tiering_{index}")
        
        uploaded_file = st.file_uploader("Upload new profile picture", type=["png", "jpg", "jpeg"], key=f"edit_pic_{index}")
        
        col_update, col_cancel = st.columns(2)
        with col_update:
            submitted = st.form_submit_button("Update Contact")
        with col_cancel:
            if st.form_submit_button("Cancel"):
                st.session_state.editing_contact_index = None # Exit edit mode
                st.rerun()

        if submitted:
            if name and designation and country and company:
                updated_contact = contact.copy() # Make a mutable copy
                
                # Check for changes and record history
                changes = []
                if name != contact["Name"]: changes.append(f"Name changed from '{contact['Name']}' to '{name}'")
                if designation != contact["Designation"]: changes.append(f"Designation changed from '{contact['Designation']}' to '{designation}'")
                if country != contact["Country"]: changes.append(f"Country changed from '{contact['Country']}' to '{country}'")
                if company != contact["Company"]: changes.append(f"Company changed from '{contact['Company']}' to '{company}'")
                if phone_number != contact["Phone Number"]: changes.append(f"Phone Number changed from '{contact['Phone Number']}' to '{phone_number}'")
                if office_number != contact["Office Number"]: changes.append(f"Office Number changed from '{contact['Office Number']}' to '{office_number}'")
                if office_address != contact["Office Address"]: changes.append(f"Office Address changed from '{contact['Office Address']}' to '{office_address}'")
                if home_address != contact["Home Address"]: changes.append(f"Home Address changed from '{contact['Home Address']}' to '{home_address}'")
                if hobbies != contact["Hobbies"]: changes.append(f"Hobbies changed from '{contact['Hobbies']}' to '{hobbies}'")
                if dietary_restrictions != contact["Dietary Restrictions"]: changes.append(f"Dietary Restrictions changed from '{contact['Dietary Restrictions']}' to '{dietary_restrictions}'")
                if celebrated_festivities != contact["Celebrated Festivities"]: changes.append(f"Celebrated Festivities changed from '{contact['Celebrated Festivities']}' to '{celebrated_festivities}'")
                if events_invited_to != contact["Events Invited To"]: changes.append(f"Events Invited To changed from '{contact['Events Invited To']}' to '{events_invited_to}'")
                if status != contact["Status"]: changes.append(f"Status changed from '{contact['Status']}' to '{status}'")
                if tiering != contact["Tiering"]: changes.append(f"Tiering changed from '{contact['Tiering']}' to '{tiering}'")

                # --- Track Profile Picture Change ---
                if uploaded_file is not None:
                    new_pic_bytes = uploaded_file.read()
                    if new_pic_bytes != contact["Profile Picture"]:
                        changes.append("Profile picture updated")
                    updated_contact["Profile Picture"] = new_pic_bytes
                elif contact["Profile Picture"] is not None and uploaded_file is None:
                    # If there was a picture and now it's removed (by not uploading a new one)
                    # This check is a bit tricky with how file_uploader behaves on re-renders without new file selection.
                    # For simplicity, we assume if uploaded_file is None but current has a pic, it wasn't explicitly removed.
                    # A more robust check might involve a "remove picture" checkbox.
                    pass # Do nothing, keep existing pic if no new one uploaded

                updated_contact["Name"] = name
                updated_contact["Designation"] = designation
                updated_contact["Country"] = country
                updated_contact["Company"] = company
                updated_contact["Phone Number"] = phone_number
                updated_contact["Office Number"] = office_number
                updated_contact["Office Address"] = office_address
                updated_contact["Home Address"] = home_address
                updated_contact["Hobbies"] = hobbies
                updated_contact["Dietary Restrictions"] = dietary_restrictions
                updated_contact["Celebrated Festivities"] = celebrated_festivities
                updated_contact["Events Invited To"] = events_invited_to
                updated_contact["Status"] = status
                updated_contact["Tiering"] = tiering
                
                # The uploaded_file logic is handled above for history tracking
                # updated_contact["Profile Picture"] = new_pic_bytes # This line moved up

                if changes:
                    # Join changes with an HTML line break for display in history
                    update_info = (f"Updated by {st.session_state.user_role} at {datetime.now().strftime('%d %b %y, %I:%M %p')}.<br>"
                                   + "<br>".join(changes))
                    updated_contact["Last Updated By"] = st.session_state.user_role
                    updated_contact["Last Updated On"] = datetime.now().strftime("%d %b %y, %I:%M %p")
                    updated_contact["History"].append(update_info)

                st.session_state.contacts_df.loc[index] = updated_contact
                st.success("Contact updated successfully!")
                st.session_state.editing_contact_index = None # Exit edit mode
                st.rerun()
            else:
                st.error("Please fill in all required fields (Name, Designation, Country, Company).")

def display_contact_card(contact, index):
    st.markdown('<div class="contact-card">', unsafe_allow_html=True)
    
    if st.session_state.editing_contact_index == index:
        edit_contact_form(contact, index)
    else:
        # Display mode
        col1, col2, col3 = st.columns([0.8, 3, 1])
        
        with col1:
            st.markdown('<div class="profile-pic-container">', unsafe_allow_html=True)
            if contact["Profile Picture"] is not None:
                try:
                    image = Image.open(io.BytesIO(contact["Profile Picture"]))
                    st.image(image, width=90)
                except:
                    # Fallback if image data is corrupted or unreadable
                    st.image("https://via.placeholder.com/90/cccccc/ffffff?text=No+Image", width=90, caption="No Image")
            else:
                # Default image when no profile picture
                st.image("https://via.placeholder.com/90/cccccc/ffffff?text=No+Image", width=90, caption="No Image")
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown(f"### {contact['Name']}")
            st.markdown(f"<p>{contact['Designation']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p>{contact['Company']}, {contact['Country']}</p>", unsafe_allow_html=True)
        
        with col3:
            tier_class = f"tier-{contact['Tiering'].replace(' ', '')}"
            status_class = f"status-{contact['Status']}"
            st.markdown(f'<div class="tier-badge {tier_class}">{contact["Tiering"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="status-badge {status_class}">{contact["Status"]}</div>', unsafe_allow_html=True)
            
        st.markdown("---")

        # Split into 3 columns
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.markdown(f'<div class="info-item"><b>Phone Number:</b> {contact["Phone Number"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="info-item"><b>Home Address:</b> {contact["Home Address"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="info-item"><b>Celebrated Festivities:</b> {contact["Celebrated Festivities"]}</div>', unsafe_allow_html=True)
        with col_b:
            st.markdown(f'<div class="info-item"><b>Office Number:</b> {contact["Office Number"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="info-item"><b>Hobbies:</b> {contact["Hobbies"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="info-item"><b>Events Invited To:</b> {contact["Events Invited To"]}</div>', unsafe_allow_html=True)
        with col_c:
            st.markdown(f'<div class="info-item"><b>Office Address:</b> {contact["Office Address"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="info-item"><b>Dietary Restrictions:</b> {contact["Dietary Restrictions"]}</div>', unsafe_allow_html=True)
            # You might have an empty slot here or re-arrange for balance

        if contact["Last Updated On"]:
            st.info(f"Last updated by {contact['Last Updated By']} at {contact['Last Updated On']}")

        if st.session_state.user_role == "admin":
            col_edit, col_history = st.columns(2)
            with col_edit:
                if st.button(f"Edit {contact['Name']}", key=f"edit_button_{index}"):
                    st.session_state.editing_contact_index = index
                    st.rerun()
            with col_history:
                with st.expander("View History"):
                    if contact["History"]:
                        for i, history_entry in enumerate(contact["History"]):
                            st.markdown(f"**{i+1}.** {history_entry}", unsafe_allow_html=True)
                    else:
                        st.write("No history available.")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("---")

# --- Add New Contact ➕ ---
def add_new_contact_form():
    st.sidebar.title("Add New Contact")
    with st.form(key="add_contact_form"):
        name = st.text_input("Name*")
        designation = st.text_input("Designation*")
        country = st.text_input("Country*")
        company = st.text_input("Company*")
        phone_number = st.text_input("Phone Number")
        office_number = st.text_input("Office Number")
        office_address = st.text_area("Office Address")
        home_address = st.text_area("Home Address")
        hobbies = st.text_input("Hobbies")
        dietary_restrictions = st.text_input("Dietary Restrictions")
        celebrated_festivities = st.text_input("Celebrated Festivities")
        events_invited_to = st.text_input("Events Invited To")
        status = st.selectbox("Status", ["Active", "Inactive"], index=0)
        tiering = st.selectbox("Tiering", ["A", "B", "C", "Untiered"], index=3)
        profile_picture = st.file_uploader("Upload Profile Picture", type=["png", "jpg", "jpeg"])

        col_add, col_cancel = st.columns(2)
        with col_add:
            submitted = st.form_submit_button("Add Contact")
        with col_cancel:
            if st.form_submit_button("Cancel"):
                st.session_state.show_add_form = False
                st.rerun()

        if submitted:
            if name and designation and country and company:
                new_profile_pic_bytes = None
                if profile_picture:
                    new_profile_pic_bytes = profile_picture.read()

                new_contact = {
                    "Name": name,
                    "Designation": designation,
                    "Country": country,
                    "Company": company,
                    "Phone Number": phone_number,
                    "Office Number": office_number,
                    "Office Address": office_address,
                    "Home Address": home_address,
                    "Hobbies": hobbies,
                    "Dietary Restrictions": dietary_restrictions,
                    "Celebrated Festivities": celebrated_festivities,
                    "Events Invited To": events_invited_to,
                    "Status": status,
                    "Tiering": tiering,
                    "Profile Picture": new_profile_pic_bytes,
                    "Last Updated By": st.session_state.user_role if st.session_state.user_role else "Unknown",
                    "Last Updated On": datetime.now().strftime("%d %b %y, %I:%M %p"),
                    "History": [f"Created by {st.session_state.user_role if st.session_state.user_role else 'Unknown'} at {datetime.now().strftime('%d %b %y, %I:%M %p')}"]
                }
                st.session_state.contacts_df = pd.concat([st.session_state.contacts_df, pd.DataFrame([new_contact])], ignore_index=True)
                st.sidebar.success("Contact added successfully!")
                st.session_state.show_add_form = False # Hide form after submission
                st.rerun()
            else:
                st.sidebar.error("Please fill in all required fields (Name, Designation, Country, Company).")

# --- 3. Search and Filter Functionality ---
def search_and_filter():
    st.sidebar.title("Search and Filter")
    search_query = st.sidebar.text_input("Search (any field)")
    show_inactive = st.sidebar.checkbox("Show Inactive Contacts")
    
    if not show_inactive:
        filtered_df = st.session_state.contacts_df[st.session_state.contacts_df["Status"] == "Active"].copy()
    else:
        filtered_df = st.session_state.contacts_df.copy()

    if search_query:
        search_query_lower = search_query.lower()
        # Exclude 'Profile Picture' column from the string conversion and search
        # Convert all other columns to string and then search
        mask = filtered_df.drop(columns=["Profile Picture"], errors='ignore').apply(
            lambda row: row.astype(str).str.lower().str.contains(search_query_lower, na=False).any(), axis=1
        )
        filtered_df = filtered_df[mask]

    filtered_df = filtered_df.sort_values(by="Country", ascending=True)
    return filtered_df

# --- 4. Admin Download Functionality ---
def download_csv():
    if st.session_state.user_role == "admin":
        st.sidebar.markdown("---")
        st.sidebar.title("Admin Actions")
        df_for_download = st.session_state.contacts_df.drop(columns=["Profile Picture", "History"], errors='ignore').copy()
        
        csv_export = df_for_download.to_csv(index=False).encode('utf-8')
        st.sidebar.download_button(
            label="Download Active Contacts as CSV",
            data=csv_export,
            file_name="active_contacts.csv",
            mime="text/csv",
            help="Downloads currently active contact data."
        )

# --- 5. Main App Logic ---
def main():
    if st.session_state.user_role is None:
        st.title("Welcome to the Contact Card App 👋")
        login()
    else:
        st.sidebar.write(f"Logged in as: **{st.session_state.user_role.capitalize()}**")
        logout()
        
        st.title("Contact Cards 📇")

        # Admin specific actions
        if st.session_state.user_role == "admin":
            download_csv()

            if st.sidebar.button("Add New Contact"):
                st.session_state.show_add_form = True
            
            if st.session_state.show_add_form:
                add_new_contact_form()

        elif st.session_state.user_role == "user":
            if st.sidebar.button("Add New Contact"):
                st.session_state.show_add_form = True
            
            if st.session_state.show_add_form:
                add_new_contact_form()
        
        st.markdown("---")

        filtered_contacts = search_and_filter()

        # Display number of contacts
        st.markdown(f"**Currently displaying {len(filtered_contacts)} contacts.**")

        if not filtered_contacts.empty:
            for index, contact in filtered_contacts.iterrows():
                display_contact_card(contact, index)
        else:
            st.info("No contacts found matching your criteria.")

if __name__ == "__main__":
    main()