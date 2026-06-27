import streamlit as st
import pandas as pd
from groq import Groq
from dotenv import load_dotenv
import os
import random

load_dotenv()
topics=["discipline","hard work","Consistency","focus","Time management","Success","motivation"]
random_topics=random.choice(topics)


client = Groq(api_key=os.getenv("GROQ_API_KEY"))
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content":f"Give me one short, powerful motivational quote about {random_topics}. Just the quote, nothing else."}
    ]
)
tip = response.choices[0].message.content




st.title("🎯 Welcome to Anti-Procrastination AI!")
st.subheader("Your personal AI-powered productivity companion")
st.subheader("💡 Tip of the Day")

st.write(tip)
st.divider()

st.write("This app helps you set goals, track your progress, and stay motivated through intelligent AI-driven insights.")

st.write("👈 Get started from the sidebar:")
st.write("📋 **Goals** — Add and manage your goals")
st.write("🤖 **AI Chat** — Get personalized motivation and guidance based on your progress")
st.write("📊 **Dashboard** — Visualize your progress with detailed analytics")

try:
    goals_df = pd.read_csv("goals.csv")
    total = len(goals_df)
    completed = len(goals_df[goals_df["Status"] == "Done"])
    
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Goals", total)
    with col2:
        st.metric("Completed", completed)
    if completed == total and total > 0:
     st.success("🎉 Amazing! You've completed all your goals!")
         
except:
    st.write("No goals yet — start by adding one!")

st.divider()
st.subheader("How It Works")
st.write("1️⃣ **Set a goal** — Add your goals with deadlines and priorities")
st.write("2️⃣ **Track progress** — Mark goals as complete when done")
st.write("3️⃣ **Get AI support** — Receive personalized motivation based on your progress")
st.write("4️⃣ **Visualize growth** — See your achievements on the dashboard")