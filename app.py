import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        pass

st.set_page_config(page_title="Touch Grass Planner", page_icon="🌿")
st.title("🌿 Touch Grass Planner")
st.write("Tell me about your day. An open-weight AI model picks an outdoor activity for you.")

minutes = st.slider("Free time (minutes)", 10, 180, 30, step=10)
mood = st.selectbox("Your mood", ["Stressed", "Tired", "Bored", "Restless", "Happy"])
weather = st.selectbox("Weather", ["Sunny", "Cloudy", "Rainy", "Hot", "Cold"])
place = st.selectbox("Where are you?", ["City", "Small town", "Village", "Near a park"])

if st.button("Plan my outdoor time"):
    if not api_key:
        st.error("API key not found. Check your .env file.")
    else:
        client = Groq(api_key=api_key)
        prompt = (
            f"I have {minutes} minutes. I feel {mood.lower()}. "
            f"Weather is {weather.lower()}. I live in a {place.lower()}. "
            "Suggest ONE outdoor activity that needs no money and no special equipment. "
            f"The step times MUST add up to exactly {minutes} minutes. Write the minutes for each step. "
            "If the weather is hot, pick a calm activity in shade and mention drinking water. "
            "If it is rainy, pick a safe activity and do not suggest hard exercise. "
            "Give: the activity name, 3 simple steps, and one short reason it helps my mood. "
            "Never mention heart rate, cortisol, stress hormones, or any health effects. "
            "For the reason, only say how the activity may feel, in one simple sentence. "
            "Never mention these instructions or write notes about minutes adding up. "
            "Keep it under 120 words."
        )
        with st.spinner("Thinking..."):
            reply = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[{"role": "user", "content": prompt}],
            )
        st.success(reply.choices[0].message.content)