import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

today=date.today()
overdue_count=0
due_today_count=0
st.title("📊 Activity")
try:
    goals_df=pd.read_csv("goals.csv")
    total_goals=len(goals_df)
    completed_goals=len(goals_df[goals_df["Status"]=="Done"])
    pending_goals=len(goals_df[goals_df["Status"]=="pending"])
    
    for index, row in goals_df.iterrows():
        if row["Status"] == "pending":
            deadline_date = pd.to_datetime(row["Time"]).date()
            if deadline_date < today:
                overdue_count += 1
            elif deadline_date == today:
                due_today_count += 1
except:
    st.write("Kindly add some goals first!")


col1,col2,col3=st.columns(3)
with col1:
    st.metric("Total Goals",total_goals)
with col2:
    st.metric("Completed",completed_goals )
with col3:
    st.metric("Pending",pending_goals)

if total_goals > 0:
    st.subheader("Overall Progress")
    st.progress(completed_goals / total_goals)
    st.write(f"{completed_goals} out of {total_goals} goals completed!")

    if overdue_count > 0:
        st.error(f"🔴 {overdue_count} goal(s) overdue!")
    if due_today_count > 0:
        st.warning(f"⚠️ {due_today_count} goal(s) due today!")

    st.subheader("📅 Upcoming Deadlines")
    pending_df = goals_df[goals_df["Status"] == "pending"].copy()
    pending_df = pending_df.sort_values("Time")
    st.dataframe(pending_df[["goals", "Time", "Priority"]])

    st.title("Graph")
    col1,col2,col3=st.columns(3)
    with col1:
        fig,ax=plt.subplots(figsize=(8,6))
        ax.pie([completed_goals,pending_goals],labels=["Completed","Pending"],autopct="%1.1f%%")
        st.pyplot(fig)
    with col2:
        category_counts=goals_df["Category"].value_counts()
        fig2,ax2=plt.subplots(figsize=(8,6))
        ax2.bar(category_counts.index,category_counts.values,color="Red")
        ax2.set_xlabel("Category", fontsize=14)
        ax2.set_ylabel("Number of Goals", fontsize=14)
        ax2.tick_params(axis='x', labelsize=12)
        st.pyplot(fig2)
    with col3:
        priority_count=goals_df["Priority"].value_counts()
        fig3,ax3=plt.subplots(figsize=(8,6))
        ax3.bar(priority_count.index,priority_count.values,color="green")
        ax3.set_xlabel("Priority",fontsize=14)
        ax3.set_ylabel("Number of goals",fontsize=14)
        ax3.tick_params(axis='x',labelsize=12)
        st.pyplot(fig3)
else:
    st.info("No goals yet — add some goals to see your progress and analytics! 🎯")