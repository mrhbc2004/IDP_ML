# Re-run code after environment reset to regenerate dataset and train model
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import joblib

# Set seed and generate enhanced dataset again
np.random.seed(42)
n = 1000
temperature = np.random.normal(30, 5, n)
voltage = np.random.normal(3.5, 0.2, n)
current = np.random.normal(1.5, 0.4, n)
ambient_temp = np.random.normal(28, 3, n)
battery_charge = np.random.uniform(20, 100, n)
temp_rise_rate = np.random.normal(0.2, 0.1, n)
temp_vs_ambient = temperature - ambient_temp
power = voltage * current

data = pd.DataFrame({
    'temperature': temperature,
    'voltage': voltage,
    'current': current,
    'ambient_temp': ambient_temp,
    'battery_charge': battery_charge,
    'temp_rise_rate': temp_rise_rate,
    'temp_vs_ambient': temp_vs_ambient,
    'power': power
})

data['overheating'] = (
    ((temp_vs_ambient > 5) & (power > 5)) |
    (temp_rise_rate > 0.3)
).astype(int)

data.loc[data.sample(frac=0.7, random_state=42).index, 'overheating'] = 0

# Save CSV
csv_path = "/mnt/data/enhanced_battery_data.csv"
data.to_csv(csv_path, index=False)

# Train model
X = data.drop("overheating", axis=1)
y = data["overheating"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
report = classification_report(y_test, y_pred, output_dict=True)
conf_matrix = confusion_matrix(y_test, y_pred)

# Save model
model_path = "/mnt/data/enhanced_battery_model.pkl"
joblib.dump(model, model_path)

model_path, report, conf_matrix.tolist()
