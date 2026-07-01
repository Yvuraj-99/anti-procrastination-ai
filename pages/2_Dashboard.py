import streamlit as st                    # Streamlit - web app banane ke liye
import pandas as pd                       # Pandas - CSV/data handle karne ke liye
import matplotlib.pyplot as plt           # Matplotlib - charts (pie, bar) banane ke liye
from datetime import date                 # date - aaj ki date nikalne ke liye

today=date.today()                        # aaj ki date store karta hai
overdue_count=0                           # overdue goals ka counter (0 se shuru)
due_today_count=0                         # due-today goals ka counter (0 se shuru)
st.title("📊 Activity")                    # Page ka title

try:                                                          # try-except - CSV na ho toh crash na ho
    goals_df=pd.read_csv("goals.csv")                         # goals.csv padhta hai
    total_goals=len(goals_df)                                 # total goals ki count
    completed_goals=len(goals_df[goals_df["Status"]=="Done"]) # "Done" status wale goals count
    pending_goals=len(goals_df[goals_df["Status"]=="pending"])# "pending" status wale goals count
    
    for index, row in goals_df.iterrows():                    # har goal (row) pe loop:
        if row["Status"] == "pending":                        # sirf pending goals ke liye:
            deadline_date = pd.to_datetime(row["Time"]).date()# deadline string ko date object banata hai
            if deadline_date < today:                         # agar deadline past mein:
                overdue_count += 1                            # overdue counter +1
            elif deadline_date == today:                      # agar deadline aaj:
                due_today_count += 1                          # due-today counter +1
except:                                                       # agar error (CSV nahi mili):
    st.write("Kindly add some goals first!")                 # friendly message dikhao


col1,col2,col3=st.columns(3)              # page ko 3 columns mein baant ta hai
with col1:                                # pehle column mein:
    st.metric("Total Goals",total_goals)  # Total Goals metric
with col2:                                # doosre column mein:
    st.metric("Completed",completed_goals )   # Completed metric
with col3:                                # teesre column mein:
    st.metric("Pending",pending_goals)    # Pending metric

if total_goals > 0:                       # agar kam se kam 1 goal hai (warna sab charts skip - empty crash avoid):
    st.subheader("Overall Progress")      # "Overall Progress" heading
    st.progress(completed_goals / total_goals)   # progress bar - completed/total = percentage (jaise 3/4 = 75%)
    st.write(f"{completed_goals} out of {total_goals} goals completed!")   # text mein progress batata hai

    if overdue_count > 0:                 # agar koi overdue goal hai:
        st.error(f"🔴 {overdue_count} goal(s) overdue!")   # red alert dikhata hai
    if due_today_count > 0:               # agar koi due-today goal hai:
        st.warning(f"⚠️ {due_today_count} goal(s) due today!")   # yellow warning dikhata hai

    st.subheader("📅 Upcoming Deadlines")  # "Upcoming Deadlines" heading
    pending_df = goals_df[goals_df["Status"] == "pending"].copy()   # sirf pending goals ki copy banata hai
    pending_df = pending_df.sort_values("Time")   # deadline ke order mein sort karta hai (paas wali upar)
    st.dataframe(pending_df[["goals", "Time", "Priority"]])   # table mein sirf goal, deadline, priority dikhata hai

    st.title("Graph")                     # "Graph" section title
    col1,col2,col3=st.columns(3)          # charts ke liye 3 columns
    with col1:                            # pehle column - Pie chart:
        fig,ax=plt.subplots(figsize=(8,6))   # figure aur axis banata hai (8x6 size)
        fig.patch.set_facecolor('black') # figure ka background black set karta hai
        ax.set_facecolor('black') # axis ka background black set karta hai
        ax.pie([completed_goals,pending_goals],labels=["Completed","Pending"],autopct="%1.1f%%")   # pie chart - completed vs pending, % ke saath
        st.pyplot(fig)                    # chart ko screen pe dikhata hai
    with col2:                            # doosre column - Category bar chart:
        category_counts=goals_df["Category"].value_counts()   # har category ke goals count karta hai
        fig2,ax2=plt.subplots(figsize=(8,6))   # naya figure/axis
        fig2.patch.set_facecolor('black') # axis ka background black set karta hai
        ax2.set_facecolor('black') # axis ka background black set karta hai
        ax2.bar(category_counts.index,category_counts.values,color="Red")   # bar chart (red) - category wise
        ax2.set_xlabel("Category", fontsize=14)   # x-axis ka label
        ax2.set_ylabel("Number of Goals", fontsize=14)   # y-axis ka label
        ax2.tick_params(axis='x', labelsize=12)   # x-axis ke numbers ka font size
        st.pyplot(fig2)                   # chart dikhata hai
    with col3:                            # teesre column - Priority bar chart:
        priority_count=goals_df["Priority"].value_counts()   # har priority ke goals count
        fig3,ax3=plt.subplots(figsize=(8,6))   # naya figure/axis
        fig3.patch.set_facecolor('black') # axis ka background black set karta hai
        ax3.set_facecolor('black') # axis ka background black set karta hai
        ax3.bar(priority_count.index,priority_count.values,color="green")   # bar chart (green) - priority wise
        ax3.set_xlabel("Priority",fontsize=14)    # x-axis label
        ax3.set_ylabel("Number of goals",fontsize=14)   # y-axis label
        ax3.tick_params(axis='x',labelsize=12)    # x-axis numbers ka font size
        st.pyplot(fig3)                   # chart dikhata hai
else:                                     # agar koi goal nahi (total_goals = 0):
    st.info("No goals yet — add some goals to see your progress and analytics! 🎯")   # friendly message (charts skip, crash avoid)