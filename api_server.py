from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load enhanced trained model
model = joblib.load("enhanced_battery_model.pkl")

# Define expected features (order matters)
FEATURES = [
    "temperature",
    "voltage",
    "current",
    "ambient_temp",
    "battery_charge",
    "temp_rise_rate",
    "temp_vs_ambient",
    "power"
]

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    # Input validation
    if not all(feature in data for feature in FEATURES):
        return jsonify({"error": "Missing one or more required fields."}), 400

    # Create DataFrame for model
    df = pd.DataFrame([[data[feature] for feature in FEATURES]], columns=FEATURES)
    
    # Predict using ML model
    prediction = int(model.predict(df)[0])

    return jsonify({"prediction": prediction})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
