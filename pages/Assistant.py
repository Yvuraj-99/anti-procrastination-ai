import streamlit as st
from groq import Groq
import pandas as pd
from dotenv import load_dotenv
import os
import time
from datetime import date
from datetime import datetime 

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.title("🤖 AI Chat")
st.markdown("""
<style>
.stChatMessage {
    border-radius: 20px;
}
[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) {
    flex-direction: row-reverse;
    justify-content: flex-end;
}
[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) > div:nth-child(2) {
    max-width: 70%;
    margin-left: auto;
}
</style>
""", unsafe_allow_html=True)

try:
    goals_df=pd.read_csv("goals.csv")
    pending_count=len(goals_df[goals_df["Status"]=="pending"])
    goal_name = ""
    today=date.today()
    for index, row in goals_df.iterrows():
     if row["Status"] == "pending":
        deadline_date= pd.to_datetime(row["Time"]).date()
        if deadline_date < today:
            tag="OVERDUE"
        elif deadline_date==today:
            tag="DUE TODAY"
        else:
            tag="On Track"
        goal_name += f"{row['goals']} (deadline: {row['Time']}, priority: {row['Priority']}, status:{tag}), "    
      
except:
    pending_count= 0    


if pending_count == 0:
    system_prompt = f"Your name is El, a supportive productivity AI. All goals are completed! The user completed these goals: {goal_name}. The priority (High/Medium/Low) is already given for each goal — use it directly, don't create your own scale. Celebrate and praise them. Respond in the same language as the goals are written in."

elif pending_count > 2:
    system_prompt = f"Your name is El, an energetic motivator. Give powerful motivation! The user's goals are: {goal_name}. The priority (High/Medium/Low) is already given for each goal — use it directly, don't create your own scale. Respond in the same language as the goals are written in."

else:
    system_prompt = f"Your name is El, a funny roaster. Give a short funny roast so the user completes their task! The user's goals are: {goal_name}. The priority (High/Medium/Low) is already given for each goal — use it directly, don't create your own scale. Respond in the same language as the goals are written in."
if "messages" not in st.session_state:
    st.session_state.messages = []
current_hour=datetime.now().hour
if current_hour <12:
        greeting ="Good Morning"
elif current_hour <17:
        greeting="Good Afternoon"
else:
        greeting="Good Evening"
if len(st.session_state.messages)==0:
    with st.chat_message("assistant"):
        st.write(f"{greeting} I'm El, your Personal Productivity Ai. Ready to crush your goals today?💪 ")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("kuch bolo:")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
    with st.spinner("Thinking...."):
     response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": system_prompt}] + st.session_state.messages
    )
    ai_reply = response.choices[0].message.content
    if pending_count==0:
        
        if"celebrated"not in st.session_state:
            st.balloons()
            st.session_state.celebrated=False


    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
    with st.chat_message("assistant"):
        def type_effect(text):
            for word in text.split():
                yield word + " "
                time.sleep(0.05)
    
        st.write_stream(type_effect(ai_reply))            
if st.button(" Clear Chat"):
    st.session_state.messages = [] 
    st.rerun()     