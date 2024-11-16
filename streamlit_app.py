import streamlit as st
import pandas as pd
import plotly.express as px

# Sample workload data (replace with your actual data)
workload_data = [
    # ... your workload data
]

def create_dashboard():
    st.title("Workload Management Dashboard")

    # Convert data to DataFrame
    df = pd.DataFrame(workload_data)

    # Group by month and count tasks
    monthly_workload = df.groupby("month").size().reset_index(name="total_tasks")

    # Create a color-coded bar chart
    fig = px.bar(monthly_workload, x="month", y="total_tasks", color_discrete_sequence=["lightblue", "orange", "red"])
    st.plotly_chart(fig)

    # Display individual workload on click
    team_members = df["team_member"].unique()
    selected_member = st.selectbox("Select Team Member", team_members)

    member_tasks = df[df["team_member"] == selected_member]
    st.dataframe(member_tasks)

if __name__ == "__main__":
    create_dashboard()