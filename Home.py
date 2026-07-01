import streamlit as st                    # Streamlit library import - web app ban ane ke liye
import pandas as pd                       # Pandas import - CSV/data handle karne ke liye
from groq import Groq                     # Groq import - AI (LLM) ko call karne ke liye
from dotenv import load_dotenv            # dotenv import - .env file se secrets padhne ke liye
import os                                 # os import - environment variables (API key) access karne ke liye
import random                             # random import - list se random choice ke liye

load_dotenv()                             # .env file load karta hai (taaki API key mile)
topics=["discipline","hard work","Consistency","focus","Time management","Success","motivation"]   # topics ki list - quote ke liye alag-alag themes
random_topics=random.choice(topics)       # list mein se ek RANDOM topic choose karta hai (har refresh pe alag)


client = Groq(api_key=os.getenv("GROQ_API_KEY"))   # Groq client banata hai, API key .env se leke
response = client.chat.completions.create(          # AI ko request bhejta hai quote ke liye
    model="openai/gpt-oss-120b",               # kaunsa AI model use karna hai (llama)
    messages=[
        {"role": "user", "content":f"Give me one short, powerful motivational quote about {random_topics}. Just the quote, nothing else."}   # AI ko instruction - random topic pe quote do (f-string se topic inject kiya)
    ]
)
tip = response.choices[0].message.content   # AI ke response mein se actual quote text nikalta hai




st.title("🎯 Welcome to Anti-Procrastination AI!")              # Page ka main title
st.subheader("Your personal AI-powered productivity companion")  # Title ke neeche subtitle
st.subheader("💡 Tip of the Day")                                # "Tip of the Day" section ka heading

st.write(tip)                             # AI se generated quote screen pe dikhata hai
st.divider()                              # ek horizontal line (visual separator)

st.write("This app helps you set goals, track your progress, and stay motivated through intelligent AI-driven insights.")   # App ka description

st.write("👈 Get started from the sidebar:")                                              # Sidebar use karne ka hint
st.write("📋 **Goals** — Add and manage your goals")                                      # Goals page ka description
st.write("🤖 **AI Chat** — Get personalized motivation and guidance based on your progress")  # AI Chat page ka description
st.write("📊 **Dashboard** — Visualize your progress with detailed analytics")            # Dashboard page ka description

try:                                                          # try-except - agar CSV na ho/error aaye toh app crash na ho
    goals_df = pd.read_csv("goals.csv")                       # goals.csv file ko padhta hai
    total = len(goals_df)                                     # total goals ki count (kitni rows hain)
    completed = len(goals_df[goals_df["Status"] == "Done"])   # sirf "Done" status wale goals count karta hai
    
    st.divider()                                              # visual separator line
    col1, col2 = st.columns(2)                                # page ko 2 columns mein baant ta hai
    with col1:                                                # pehle column mein:
        st.metric("Total Goals", total)                       # "Total Goals" metric dikhata hai
    with col2:                                                # doosre column mein:
        st.metric("Completed", completed)                     # "Completed" metric dikhata hai
    if completed == total and total > 0:                      # agar SAB goals complete hain AUR kam se kam 1 goal hai
     st.success("🎉 Amazing! You've completed all your goals!")   # toh celebration message dikhao
         
except:                                                       # agar upar koi error aaya (jaise CSV nahi mili):
    st.write("No goals yet — start by adding one!")           # toh yeh friendly message dikhao

st.divider()                              # visual separator line
st.subheader("How It Works")              # "How It Works" section ka heading
st.write("1️⃣ **Set a goal** — Add your goals with deadlines and priorities")              # Step 1 explanation
st.write("2️⃣ **Track progress** — Mark goals as complete when done")                      # Step 2 explanation
st.write("3️⃣ **Get AI support** — Receive personalized motivation based on your progress")  # Step 3 explanation
st.write("4️⃣ **Visualize growth** — See your achievements on the dashboard")              # Step 4 explanation










