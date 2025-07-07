import streamlit as st
import joblib
import pandas as pd

# Load trained model
model = joblib.load('battery_model.pkl')

st.set_page_config(page_title="Smart Battery Cooling System", layout="centered")
st.title("🔋 Smart Battery Cooling System - AI Decision")
st.write("Use the sliders below to simulate sensor inputs and check if cooling is required.")

# Input sliders
temperature = st.slider("Battery Temperature (°C)", 20, 80, 40)
voltage = st.slider("Battery Voltage (V)", 3.0, 4.5, 3.7)
current = st.slider("Battery Current (A)", 0.0, 5.0, 1.5)
ambient_temp = st.slider("Ambient Temperature (°C)", 10, 50, 30)
battery_charge = st.slider("Battery Charge (%)", 0, 100, 50)

# When user clicks the button
if st.button("🔍 Check Cooling Status"):
    input_df = pd.DataFrame([{
        'temperature': temperature,
        'voltage': voltage,
        'current': current,
        'ambient_temp': ambient_temp,
        'battery_charge': battery_charge
    }])

    # Optional: Show input
    st.write("📥 Sensor Input Data:")
    st.dataframe(input_df)

    # Get prediction
    prediction = model.predict(input_df)[0]

    # Optional: View probability
    prediction_proba = model.predict_proba(input_df)[0]

# Check how many classes exist in model
    if len(prediction_proba) == 2:
        st.write(f"🧠 Model Confidence → Safe: {prediction_proba[0]*100:.1f}% | Overheat: {prediction_proba[1]*100:.1f}%")
    else:
        st.write(f"🧠 Model Confidence → {prediction_proba[0]*100:.1f}% (Only one class in training data)")
