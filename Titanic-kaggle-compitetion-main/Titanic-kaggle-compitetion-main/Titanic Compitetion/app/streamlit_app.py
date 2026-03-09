import sys
import os
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

import streamlit as st
import pandas as pd
import requests
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from src.utils.logger import setup_logger

logger = setup_logger("Streamlit")

st.set_page_config(page_title="Spaceship Titanic Predictor", page_icon="🚀", layout="wide")

# Theme / Background Settings
# Custom glassmorphism or vibrant styling can be added via CSS
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #1e1e2f 0%, #2a2a40 100%);
        color: white;
    }
    .stButton>button {
        background-color: #4a90e2;
        color: white;
        border-radius: 8px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.title("🚀 Spaceship Titanic Predictor 🚢")
st.write("Determine the fate of passengers on the interstellar voyage!")

# Sidebar for Passenger Input
st.sidebar.header("Passenger Details")

passenger_id = st.sidebar.text_input("Passenger ID", "0001_01")
home_planet = st.sidebar.selectbox("Home Planet", ["Earth", "Europa", "Mars"])
destination = st.sidebar.selectbox("Destination", ["TRAPPIST-1e", "PSO J318.5-22", "55 Cancri e"])
cryo_sleep = st.sidebar.checkbox("CryoSleep", False)
cabin = st.sidebar.text_input("Cabin (Deck/Num/Side)", "B/0/P")
age = st.sidebar.slider("Age", 0, 80, 25)
vip = st.sidebar.checkbox("VIP Status", False)

st.sidebar.subheader("Spending Onboard")
room_service = st.sidebar.number_input("Room Service ($)", 0.0, 10000.0, 0.0)
food_court = st.sidebar.number_input("Food Court ($)", 0.0, 10000.0, 0.0)
shopping_mall = st.sidebar.number_input("Shopping Mall ($)", 0.0, 10000.0, 0.0)
spa = st.sidebar.number_input("Spa ($)", 0.0, 10000.0, 0.0)
vr_deck = st.sidebar.number_input("VR Deck ($)", 0.0, 10000.0, 0.0)

# Build input dictionary
passenger_data = {
    "PassengerId": passenger_id,
    "HomePlanet": home_planet,
    "CryoSleep": cryo_sleep,
    "Cabin": cabin,
    "Destination": destination,
    "Age": age,
    "VIP": vip,
    "RoomService": room_service,
    "FoodCourt": food_court,
    "ShoppingMall": shopping_mall,
    "Spa": spa,
    "VRDeck": vr_deck,
    "Name": "Sample Name"
}

# Prediction Logic
if st.button("🔮 Predict Transport Status"):
    API_URL = "http://localhost:8000/predict"
    
    try:
        st.info("Contacting Predictor API...")
        response = requests.post(API_URL, json=passenger_data, timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            is_transported = result["is_transported"]
            probability = result.get("probability", 0.5)
            
            if is_transported:
                st.balloons()
                st.success(f"✅ Prediction: **TRANSPORTED** (Prob: {probability:.2f}) 🌀")
            else:
                st.error(f"❌ Prediction: **NOT TRANSPORTED** (Prob: {1-probability:.2f}) ☄️")
        else:
            st.warning(f"API returned error: {response.text}. Falling back to local simulation.")
            import random
            if random.choice([True, False]):
                st.success("✅ Prediction: **TRANSPORTED** (Simulated) 🌀")
            else:
                st.error("❌ Prediction: **NOT TRANSPORTED** (Simulated) ☄️")
                
    except Exception as e:
        logger.error(f"API connection failed: {e}")
        st.warning("Could not connect to FastAPI. Ensure it is running with `uvicorn api.fastapi_app:app`. Falling back to simulation.")
        import random
        if random.choice([True, False]):
            st.success("✅ Prediction: **TRANSPORTED** (Simulated) 🌀")
        else:
            st.error("❌ Prediction: **NOT TRANSPORTED** (Simulated) ☄️")


# Visualization Section (Global Analysis)
st.divider()
st.subheader("📊 Global Model Insights")
col1, col2 = st.columns(2)

with col1:
    st.write("### SHAP Feature Importance")
    # if os.path.exists("reports/shap/shap_summary.png"):
    #     st.image("reports/shap/shap_summary.png")
    # else:
    st.info("Train the model using `python main.py` to see actual feature importance.")

with col2:
    st.write("### Data Drift Monitoring")
    # if os.path.exists("reports/drift/drift_report.html"):
    #     st.write("[View Detailed Drift Report](file:///reports/drift/drift_report.html)")
    # else:
    st.info("Run the training pipeline to generate drift reports.")
