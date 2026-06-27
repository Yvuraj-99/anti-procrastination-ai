import streamlit as st                    # Streamlit - web app banane ke liye
import pandas as pd                       # Pandas - CSV/data handle karne ke liye
from datetime import date                 # date - aaj ki date nikalne ke liye (deadline compare)

st.title("🎯 Goals Setting")              # Page ka title
goal=st.text_input("Goal kya hai?")       # text input box - goal ka naam type karne ke liye
deadline=st.date_input("Deadline:")       # date picker - deadline choose karne ke liye
category = st.selectbox("Category:" ,["Study","Coding","Health","other"])   # dropdown - category choose karne ke liye

priority = st.selectbox("Priority", ["🔴 High", "🟡 Medium", "🟢 Low"])   # dropdown - priority choose karne ke liye
status="pending"                          # naya goal hamesha "pending" status se shuru hota hai
if st.button("Save"):                     # agar "Save" button daba:
 if goal=="":                             # agar goal field KHALI hai:
  st.error("Please enter your goal first")   # error dikhao (validation - khali goal save na ho)
 else:                                    # agar goal bhara hua hai:
  task={                                  # ek dictionary banata hai goal ke saare data ka
        "goals":goal,                     # goal ka naam
        "Time":deadline,                  # deadline
        "Category":category,              # category
        "Priority":priority,              # priority
        "Status":status                   # status (pending)
    }
  df=pd.DataFrame([task])                 # dictionary ko DataFrame (table) mein convert karta hai
  try:                                    # try-except - agar CSV pehle se hai toh usme add karo
    existing = pd.read_csv("goals.csv")   # purani goals.csv padhta hai
    df=pd.concat([existing,df], ignore_index=True)   # purane goals + naya goal jodta hai
  except:                                 # agar CSV nahi hai (pehla goal):
   pass                                   # kuch mat karo (sirf naya df use hoga)

  df.to_csv("goals.csv",index=False)      # data ko goals.csv mein save karta hai
  st.success("Goals saved")               # success message dikhata hai

st.subheader("Your Goals")                # "Your Goals" heading
try:                                                          # try-except - CSV na ho toh crash na ho
 all_goals=pd.read_csv("goals.csv")                           # saari goals padhta hai
 st.dataframe(all_goals)                                      # poori table dikhata hai
 for index , row in all_goals.iterrows():                     # har goal (row) pe loop:
  if row["Status"] == "pending":                              # sirf pending goals ke liye:
   st.write(row["goals"])                                     # goal ka naam dikhata hai
   deadline_date=pd.to_datetime(row["Time"]).date()           # deadline string ko date object banata hai
   today=date.today()                                         # aaj ki date

   if deadline_date <today:                                   # agar deadline past mein:
    st.error("🔴Overdue!")                                    # red overdue alert
   elif deadline_date == today:                               # agar deadline aaj:
    st.warning("⚠️ Due Today!")                               # yellow due-today warning
   col1,col2,col3=st.columns(3)                               # 3 columns (Delete/Complete/Edit buttons ke liye)
   with col1:                                                 # pehla column - Delete button:
    if st.button("Delete", key=f"delete_{index}", type="primary"):   # unique key ke saath delete button (red)
     all_goals=all_goals.drop(index)                          # us goal ko table se hata deta hai
     all_goals.to_csv("goals.csv",index=False)                # updated data save karta hai
     st.success("Goal deleted")                               # success message
     st.rerun()                                               # page refresh (turant update dikhe - 1 click fix)
    
   with col2:                                                 # doosra column - Complete button:
    if st.button("complete", key =index ):                    # unique key ke saath complete button
    
     all_goals.loc[index,"Status"]="Done"                     # us goal ka status "Done" kar deta hai
     all_goals.to_csv("goals.csv",index=False)                # updated data save
     st.success("Marked as completed")                        # success message
     st.rerun()                                               # page refresh (1 click fix)
   with col3:                                                 # teesra column - Edit button:
    if st.button("Edit",key=f"edit_{index}"):                 # unique key ke saath edit button
      st.session_state.edit_index= index                      # us goal ka index session mein save (kaunsa edit ho raha hai)
      st.rerun()                                              # page refresh (edit form dikhe)
 if"edit_index" in st.session_state:                          # agar koi Edit button daba (loop ke BAHAR - ek hi baar dikhe):
      st.divider()                                            # separator line
      st.subheader("✏️ Edit Goals")                           # "Edit Goals" heading
      edit_idx=st.session_state.edit_index                    # kaunsa goal edit ho raha hai uska index
      new_goal=st.text_input("Goal",value=all_goals.loc[edit_idx,"goals"])   # goal input (current value pehle se bhari)
      new_priority=st.selectbox("Priority",["🔴High","🟡Medium","🟢Low"])   # priority dropdown
      new_deadline=st.date_input('Deadline')                  # deadline picker
      if st.button("Save Changes"):                           # agar "Save Changes" daba:
       
       all_goals.loc[edit_idx,"goals"]=new_goal               # goal ka naam update
       all_goals.loc[edit_idx,"Priority"]=new_priority        # priority update
       all_goals.loc[edit_idx,"Time"]=str(new_deadline)       # deadline update (str() se string banaya - type error fix)
       all_goals.to_csv("goals.csv",index=False)              # updated data save
       del st.session_state.edit_index                        # edit mode band karta hai (session se hata)
       st.success("Goal Update")                              # success message
       st.rerun()                                             # page refresh
 Pend= all_goals[all_goals["Status"]=="pending"]              # sirf pending goals filter karta hai
 completed=all_goals[all_goals["Status"]=="Done"]             # sirf completed goals filter karta hai

 st.subheader("⏳ Pending Goals")                             # "Pending Goals" heading
 st.dataframe(Pend)                                           # pending goals ki table

 st.subheader("✅ Completed Goals")                           # "Completed Goals" heading
 st.dataframe(completed)                                      # completed goals ki table
except:                                                       # agar error (CSV nahi mili):
 st.write("Kindly save your goal first")                     # friendly message dikhao