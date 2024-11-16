import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Sample workload data for 12-month period (replace with your actual data)
workload_data = [
    {
        "team_member": "Alice", 
        "month": "Jan-2023", 
        "task": "Task 1", 
        "priority": "high"
    },
    {
        "team_member": "Bob", 
        "month": "Feb-2023", 
        "task": "Task 2", 
        "priority": "low"
    },
    {
        "team_member": "Charlie", 
        "month": "Mar-2023", 
        "task": "Task 3", 
        "priority": "medium"
    },
    {
        "team_member": "David", 
        "month": "Apr-2023", 
        "task": "Task 4", 
        "priority": "high"
    },
    {
        "team_member": "Emily", 
        "month": "May-2023", 
        "task": "Task 5", 
        "priority": "low"
    },
    {
        "team_member": "Frank", 
        "month": "Jun-2023", 
        "task": "Task 6", 
        "priority": "medium"
    },
    {
        "team_member": "Grace", 
        "month": "Jul-2023", 
        "task": "Task 7", 
        "priority": "high"
    },
    {
        "team_member": "Henry", 
        "month": "Aug-2023", 
        "task": "Task 8", 
        "priority": "low"
    },
    {
        "team_member": "Iris", 
        "month": "Sep-2023", 
        "task": "Task 9", 
        "priority": "medium"
    },
    {
        "team_member": "Jack", 
        "month": "Oct-2023", 
        "task": "Task 10", 
        "priority": "high"
    },
    {
        "team_member": "Kelly", 
        "month": "Nov-2023", 
        "task": "Task 11", 
        "priority": "low"
    },
    {
        "team_member": "Liam", 
        "month": "Dec-2023", 
        "task": "Task 12", 
        "priority": "medium"
    },
]

def create_dashboard():
    st.title("Workload Management Dashboard")

    # # Convert data to DataFrame
    df = pd.DataFrame(workload_data)

    # # Group by month and count tasks
    # #monthly_workload = df.groupby("month").size().reset_index(name="total_tasks")

    # # Group by 6-month periods and count tasks
    # df['six_month_period'] = df['month'].apply(lambda x: f"{x[:3]} - {x[4:]}")
    # monthly_workload = df.groupby("six_month_period").size().reset_index(name="total_tasks")

    # # Create a color-coded bar chart
    # fig = px.bar(monthly_workload, x="six_month_period", y="total_tasks", color_discrete_sequence=["lightblue", "orange", "red"])
    # st.plotly_chart(fig)

    # # Display individual workload on click
    # team_members = df["team_member"].unique()
    # selected_member = st.selectbox("Select Team Member", team_members)

    # member_tasks = df[df["team_member"] == selected_member]
    # st.dataframe(member_tasks)

    # Group data by team member and month
    grouped_df = df.groupby(['team_member', 'month']).size().reset_index(name='task_count')

    # Create a figure
    fig = go.Figure()

    # Add traces for each team member
    for member in grouped_df['team_member'].unique():
        member_df = grouped_df[grouped_df['team_member'] == member]
        fig.add_trace(go.Bar(
            x=member_df['month'],
            y=member_df['task_count'],
            name=member
        ))

    # Add annotations for each bar
    for i, row in grouped_df.iterrows():
        fig.add_annotation(
            x=row['month'],
            y=row['task_count'],
            text=str(row['task_count']),
            showarrow=False
        )

    fig.update_layout(
        title='Team Member Workload by Month',
        xaxis=dict(
            tickformat="%b-%y"
        )
    )

    st.plotly_chart(fig)

if __name__ == "__main__":
    create_dashboard()