import streamlit as st
import joblib
import numpy as np
import requests
import pandas as pd
import time
import random
import folium
from streamlit_folium import st_folium

# Load trained Random Forest model
model = joblib.load("depression_rf_model.pkl")

# Define tailored recommendations
recommendations = {
    "Normal": [
        "✅ Stay socially active and engaged!",
        "🥗 Maintain a balanced diet for a healthier mind",
        "💤 Ensure you have a proper sleep schedule",
        "🏋️‍♂️ Exercise regularly to boost mental well-being",
    ],
    "Mild": [
        "🧘 Try daily mindfulness or meditation sessions",
        "📵 Reduce excessive screen time to lower stress",
        "🏃 Engage in physical activities like walking or jogging",
        "🎶 Listen to calming music or take up a hobby",
    ],
    "Moderate": [
        "🧠 Use Cognitive Behavioral Therapy (CBT) techniques",
        "🤝 Join a support group for shared experiences",
        "💬 Consider professional therapy sessions",
        "✍️ Maintain a gratitude journal to track positive experiences",
    ],
    "Severe": [
        "🚨 Seek immediate psychiatric help without hesitation",
        "🏥 Consult a professional for personalized guidance",
        "❤️ Stay connected with loved ones for emotional support",
        "🛑 Avoid isolation—try talking to a close friend or counselor",
    ],
}

# Function to Get Coordinates of a City
def get_lat_lon_from_city(city):
    """Fetch latitude and longitude for a given city."""
    try:
        url = f"https://nominatim.openstreetmap.org/search?format=json&q={city}"
        headers = {"User-Agent": "StreamlitApp/1.0 (contact@example.com)"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200 and response.json():
            data = response.json()[0]
            return float(data["lat"]), float(data["lon"])
        else:
            return None, None
    except Exception as e:
        st.error(f"Error fetching location for {city}: {e}")
        return None, None

# Function to Fetch Nearby Psychiatrists
def get_nearby_psychiatrists(city):
    """Fetch nearby psychiatrists within the detected city."""
    search_terms = ["psychiatrist", "mental health clinic", "doctor", "hospital"]
    results = []
    headers = {"User-Agent": "StreamlitApp/1.0 (contact@example.com)"}
    
    for term in search_terms:
        try:
            url = f"https://nominatim.openstreetmap.org/search?format=json&q={term} in {city}"
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                continue
            response_json = response.json()
            for place in response_json[:5]:
                results.append({
                    "Name": place.get("display_name", "Unknown"),
                    "Latitude": float(place.get("lat", "0")),
                    "Longitude": float(place.get("lon", "0")),
                })
            if results:
                break
        except Exception as e:
            st.error(f"Unexpected error: {e}")
            return None
    return results if results else None

# Navigation Bar
st.set_page_config(page_title="Mental Health Check", page_icon="🧠", layout="wide")
st.sidebar.title("🔍 Navigation")
page = st.sidebar.selectbox("Go to", ["🏡 Home", "📋 Assessment", "📊 Results", "🏥 Professional Help"])
def get_level_from_score(score):
    if score < 5:
        return "Normal"
    elif score < 10:
        return "Mild"
    elif score < 15:
        return "Moderate"
    else:
        return "Severe"
if page == "🏡 Home":
    st.title("🧠 Mental Health Check - Gamified")
    st.write("Welcome! This app helps assess your mental health using a gamified PHQ-9 questionnaire and behavioral tests.")
    st.write("Use the sidebar to navigate through different sections.")


elif page == "📋 Assessment":
    st.title("📋 PHQ-9 & Behavioral Assessment")
    city = st.text_input("Enter Your City Name:", "Delhi")
    
    # Expanded PHQ-9 Questionnaire
    st.subheader("🧠 PHQ-9 Questionnaire (Last 2 Weeks)")
    phq_questions = [
        "You've stopped enjoying your favorite hobbies or spending time with loved ones.",
        "You've been feeling persistently down or hopeless lately.",
        "You often find it hard to fall asleep or wake up too early and can't sleep again.",
        "You’ve been constantly tired, even after resting.",
        "You’ve either lost your appetite or are eating much more than usual.",
        "You feel like you're a burden or not good enough.",
        "You’re struggling to focus on tasks at work or school.",
        "Others have noticed you’re either moving or speaking slower/faster than usual.",
        "You’ve had thoughts of hurting yourself or that life isn't worth it.",
        "You’ve been feeling anxious about everything lately.",
        "You've started withdrawing from social situations and people.",
        "You often experience body pain without a clear cause.",
        "You’re finding it hard to manage even simple daily routines.",
    ]
    
    phq_responses = []
    response_mapping = {"😃 Never": 0, "🙂 Sometimes": 1, "😕 Often": 2, "😢 Always": 3}
    
    for q in phq_questions:
        response = st.radio(q, ["😃 Never", "🙂 Sometimes", "😕 Often", "😢 Always"], horizontal=True)
        phq_responses.append(response_mapping[response])
    
    total_phq_score = sum(phq_responses)
    
    if st.button("🔍 Get Results"):
        st.session_state["responses"] = phq_responses + [total_phq_score]
        st.session_state["city"] = city
        st.rerun()

elif page == "📊 Results":
    st.title("📊 Prediction & Tailored Recommendations")
    if "responses" in st.session_state:
        features = np.array(st.session_state["responses"][:-1]).reshape(1, -1)  # Removing the last feature

        prediction = model.predict(features)[0]
        print(prediction)

        score = st.session_state["responses"][-1]
        level = get_level_from_score(score)
        st.subheader(f"🩺 Predicted Depression Level: **{level}**")
     #   st.subheader(f"🩺 Predicted Depression Level: **{prediction}**")
        
        # Tailored Recommendations
        st.write("Here are your personalized recommendations:")
        for advice in recommendations[prediction]:
            st.write(f"- {advice}")
    else:
        st.write("❌ No assessment data found. Complete the test first.")

elif page == "🏥 Professional Help":
    st.title("🏥 Find Nearby Psychiatrists")
    if "city" in st.session_state:
        lat, lon = get_lat_lon_from_city(st.session_state["city"])
        if lat and lon:
            psychiatrists = get_nearby_psychiatrists(st.session_state["city"])
            if psychiatrists:
                m = folium.Map(location=[lat, lon], zoom_start=12)
                for p in psychiatrists:
                    folium.Marker([p["Latitude"], p["Longitude"]], tooltip=p["Name"]).add_to(m)

                st_folium(m)
            else:
                st.warning("No psychiatrists found.")
