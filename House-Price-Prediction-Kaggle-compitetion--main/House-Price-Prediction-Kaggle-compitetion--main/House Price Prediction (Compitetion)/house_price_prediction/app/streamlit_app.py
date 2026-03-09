import streamlit as st
import pandas as pd
import joblib
import numpy as np

# Load the saved model
@st.cache_resource
def load_model():
    return joblib.load("models/saved_models/best_model.joblib")

def main():
    st.set_page_config(page_title="House Price Predictor 2026", layout="wide")
    
    st.title("🏙️ Premium House Price Prediction System")
    st.markdown("---")
    
    st.sidebar.header("Input House Features")
    
    # Input fields based on the dataset columns
    area = st.sidebar.number_input("Total Area (sqft)", min_value=500, max_value=20000, value=5000)
    bedrooms = st.sidebar.slider("Number of Bedrooms", 1, 6, 3)
    bathrooms = st.sidebar.slider("Number of Bathrooms", 1, 4, 2)
    stories = st.sidebar.slider("Number of Stories", 1, 4, 1)
    parking = st.sidebar.slider("Parking Spaces", 0, 3, 1)
    
    mainroad = st.sidebar.selectbox("Main Road Access", ["yes", "no"])
    guestroom = st.sidebar.selectbox("Has Guestroom", ["yes", "no"])
    basement = st.sidebar.selectbox("Has Basement", ["yes", "no"])
    hotwaterheating = st.sidebar.selectbox("Has Hot Water Heating", ["yes", "no"])
    airconditioning = st.sidebar.selectbox("Has Air Conditioning", ["yes", "no"])
    prefarea = st.sidebar.selectbox("Is in Preferred Area", ["yes", "no"])
    furnishingstatus = st.sidebar.selectbox("Furnishing Status", ["furnished", "semi-furnished", "unfurnished"])
    
    # Create input dataframe
    input_data = pd.DataFrame({
        'area': [area],
        'bedrooms': [bedrooms],
        'bathrooms': [bathrooms],
        'stories': [stories],
        'mainroad': [mainroad],
        'guestroom': [guestroom],
        'basement': [basement],
        'hotwaterheating': [hotwaterheating],
        'airconditioning': [airconditioning],
        'parking': [parking],
        'prefarea': [prefarea],
        'furnishingstatus': [furnishingstatus]
    })
    
    st.subheader("Selected House Configuration")
    st.write(input_data)
    
    if st.button("Predict Price"):
        try:
            model = load_model()
            prediction = model.predict(input_data)
            
            st.success(f"### Estimated Market Price: ${prediction[0]:,.2f}")
            
            # Show aesthetic metrics
            col1, col2, col3 = st.columns(3)
            col1.metric("Price per sqft", f"${prediction[0]/area:,.2f}")
            col2.metric("Size Rank", "Premium" if area > 5000 else "Standard")
            col3.metric("Modernity", "High" if airconditioning == "yes" else "Standard")
            
        except Exception as e:
            st.error(f"Error making prediction: {e}. Ensure you have trained the model first by running `python main.py`.")

if __name__ == "__main__":
    main()
