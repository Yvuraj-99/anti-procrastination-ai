import streamlit as st
import pandas as pd
from datetime import date

st.title("🎯 Goals Setting")
goal=st.text_input("Goal kya hai?")
deadline=st.date_input("Deadline:")
category = st.selectbox("Category:" ,["Study","Coding","Health","other"])

priority = st.selectbox("Priority", ["🔴 High", "🟡 Medium", "🟢 Low"])
status="pending"
if st.button("Save"):
 if goal=="":
  st.error("Please enter your goal first")
 else: 
  task={
        "goals":goal,
        "Time":deadline,
        "Category":category,
        "Priority":priority,
        "Status":status
    }
  df=pd.DataFrame([task])
  try:
    existing = pd.read_csv("goals.csv")
    df=pd.concat([existing,df], ignore_index=True)
  except:
   pass

  df.to_csv("goals.csv",index=False)
  st.success("Goals saved")

st.subheader("Your Goals")
try:
 all_goals=pd.read_csv("goals.csv")
 st.dataframe(all_goals)
 for index , row in all_goals.iterrows():
  if row["Status"] == "pending":
   st.write(row["goals"])
   deadline_date=pd.to_datetime(row["Time"]).date()
   today=date.today()

   if deadline_date <today:
    st.error("🔴Overdue!")
   elif deadline_date == today:
    st.warning("⚠️ Due Today!")
   col1,col2,col3=st.columns(3)
   with col1:
    if st.button("Delete", key=f"delete_{index}", type="primary"):
     all_goals=all_goals.drop(index)
     all_goals.to_csv("goals.csv",index=False) 
     st.success("Goal deleted")
     st.rerun()
    
   with col2:
    if st.button("complete", key =index ):
    
     all_goals.loc[index,"Status"]="Done"
     all_goals.to_csv("goals.csv",index=False)
     st.success("Marked as completed")
     st.rerun()
   with col3:
    if st.button("Edit",key=f"edit_{index}"):
      st.session_state.edit_index= index
      st.rerun()
 if"edit_index" in st.session_state:
      st.divider()
      st.subheader("✏️ Edit Goals")
      edit_idx=st.session_state.edit_index
      new_goal=st.text_input("Goal",value=all_goals.loc[edit_idx,"goals"])
      new_priority=st.selectbox("Priority",["🔴High","🟡Medium","🟢Low"])
      new_deadline=st.date_input('Deadline')
      if st.button("Save Changes"):
       
       all_goals.loc[edit_idx,"goals"]=new_goal
       all_goals.loc[edit_idx,"Priority"]=new_priority
       all_goals.loc[edit_idx,"Time"]=str(new_deadline)
       all_goals.to_csv("goals.csv",index=False)
       del st.session_state.edit_index
       st.success("Goal Update")
       st.rerun()
 Pend= all_goals[all_goals["Status"]=="pending"]
 completed=all_goals[all_goals["Status"]=="Done"]

 st.subheader("⏳ Pending Goals")
 st.dataframe(Pend)

 st.subheader("✅ Completed Goals")
 st.dataframe(completed) 
except:
 st.write("Kindly save your goal first")


