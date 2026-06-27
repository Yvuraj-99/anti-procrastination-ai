import streamlit as st                    # Streamlit - web app banane ke liye
from groq import Groq                     # Groq - AI (LLM) ko call karne ke liye
import pandas as pd                       # Pandas - CSV/data handle karne ke liye
from dotenv import load_dotenv            # dotenv - .env file se secrets padhne ke liye
import os                                 # os - environment variables (API key) access ke liye
import time                               # time - typing animation mein delay (sleep) ke liye
from datetime import date                 # date - aaj ki date nikalne ke liye (deadline compare)
from datetime import datetime             # datetime - current time/hour nikalne ke liye (greeting)

load_dotenv()                             # .env file load karta hai (API key milti hai)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))   # Groq client banata hai, API key .env se leke

st.title("🤖 AI Chat")                     # Page ka title
# Neeche CSS styling hai - chat bubbles ko rounded banane aur user messages ko right align karne ke liye
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
""", unsafe_allow_html=True)               # unsafe_allow_html=True - HTML/CSS allow karne ke liye zaroori

try:                                                          # try-except - CSV na ho toh crash na ho
    goals_df=pd.read_csv("goals.csv")                         # goals.csv padhta hai
    pending_count=len(goals_df[goals_df["Status"]=="pending"])   # pending goals ki count nikalta hai
    goal_name = ""                                            # khali string - isme saare goals ka data jodenge
    today=date.today()                                        # aaj ki date
    for index, row in goals_df.iterrows():                    # har goal (row) pe loop chalata hai
     if row["Status"] == "pending":                           # sirf pending goals ke liye:
        deadline_date= pd.to_datetime(row["Time"]).date()     # CSV ki deadline (string) ko date object banata hai
        if deadline_date < today:                             # agar deadline past mein hai:
            tag="OVERDUE"                                     # tag = OVERDUE
        elif deadline_date==today:                            # agar deadline aaj hai:
            tag="DUE TODAY"                                   # tag = DUE TODAY
        else:                                                 # warna (future deadline):
            tag="On Track"                                    # tag = On Track
        goal_name += f"{row['goals']} (deadline: {row['Time']}, priority: {row['Priority']}, status:{tag}), "    # goal ka pura data (naam+deadline+priority+tag) string mein jodta hai
      
except:                                                       # agar error aaya (CSV nahi mili):
    pending_count= 0                                          # pending_count ko 0 set kar deta hai


if pending_count == 0:                                        # agar koi pending goal nahi (sab complete):
    system_prompt = f"Your name is El, a supportive productivity AI. All goals are completed! The user completed these goals: {goal_name}. The priority (High/Medium/Low) is already given for each goal — use it directly, don't create your own scale. Celebrate and praise them. Respond in the same language as the goals are written in."   # CELEBRATE mode ka prompt

elif pending_count > 2:                                       # agar 2 se zyada pending goals:
    system_prompt = f"Your name is El, an energetic motivator. Give powerful motivation! The user's goals are: {goal_name}. The priority (High/Medium/Low) is already given for each goal — use it directly, don't create your own scale. Respond in the same language as the goals are written in."   # MOTIVATE mode ka prompt

else:                                                         # warna (1-2 pending goals):
    system_prompt = f"Your name is El, a funny roaster. Give a short funny roast so the user completes their task! The user's goals are: {goal_name}. The priority (High/Medium/Low) is already given for each goal — use it directly, don't create your own scale. Respond in the same language as the goals are written in."   # ROAST mode ka prompt

if "messages" not in st.session_state:                        # agar chat history abhi exist nahi karti:
    st.session_state.messages = []                            # khali list banata hai (history store karne ke liye)
current_hour=datetime.now().hour                              # abhi ka hour (0-23) nikalta hai
if current_hour <12:                                          # 12 se pehle:
        greeting ="Good Morning"                              # greeting = Good Morning
elif current_hour <17:                                        # 12-17 ke beech:
        greeting="Good Afternoon"                             # greeting = Good Afternoon
else:                                                         # 17 ke baad:
        greeting="Good Evening"                               # greeting = Good Evening
if len(st.session_state.messages)==0:                         # agar chat khali hai (pehli baar):
    with st.chat_message("assistant"):                        # AI ke message ke roop mein:
        st.write(f"{greeting} I'm El, your Personal Productivity Ai. Ready to crush your goals today?💪 ")   # time-based greeting dikhata hai

for msg in st.session_state.messages:                         # purane saare messages pe loop:
    with st.chat_message(msg["role"]):                        # us message ke role (user/assistant) ke saath:
        st.write(msg["content"])                              # message ka content dikhata hai

user_input = st.chat_input("kuch bolo:")                      # chat input box - user yahan type karta hai

if user_input:                                                # agar user ne kuch type kiya:
    st.session_state.messages.append({"role": "user", "content": user_input})   # user ka message history mein add
    with st.chat_message("user"):                             # user message ke roop mein:
        st.write(user_input)                                  # user ka input dikhata hai
    with st.spinner("Thinking...."):                          # "Thinking..." spinner dikhata hai jab tak AI soch raha hai
     response = client.chat.completions.create(               # AI ko request bhejta hai
        model="llama-3.3-70b-versatile",                      # kaunsa model
        messages=[{"role": "system", "content": system_prompt}] + st.session_state.messages   # system prompt + poori chat history bhejta hai
    )
    ai_reply = response.choices[0].message.content            # AI ke response se actual reply text nikalta hai
    if pending_count==0:                                      # agar sab goals complete:
        
        if"celebrated"not in st.session_state:                # agar abhi tak celebrate nahi hua:
            st.balloons()                                     # balloons animation dikhata hai
            st.session_state.celebrated=False                 # celebrated flag set karta hai (taaki dobara na ho)


    st.session_state.messages.append({"role": "assistant", "content": ai_reply})   # AI ka reply history mein add
    with st.chat_message("assistant"):                        # AI message ke roop mein:
        def type_effect(text):                                # typing animation ke liye function
            for word in text.split():                         # reply ke har word pe loop:
                yield word + " "                              # ek-ek word de ke (yield)
                time.sleep(0.05)                              # har word ke baad 0.05 sec rukता hai (typing effect)
    
        st.write_stream(type_effect(ai_reply))                # typing effect ke saath reply dikhata hai
if st.button(" Clear Chat"):                                  # agar "Clear Chat" button daba:
    st.session_state.messages = []                            # chat history khali kar deta hai
    st.rerun()                                                # page refresh karta hai (turant clear dikhe)