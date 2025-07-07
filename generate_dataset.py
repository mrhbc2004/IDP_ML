import pandas as pd
import numpy as np

# Set seed for reproducibility
np.random.seed(42)
n = 1000

# Generate enhanced synthetic data
temperature = np.random.normal(30, 5, n)
voltage = np.random.normal(3.5, 0.2, n)
current = np.random.normal(1.5, 0.4, n)
ambient_temp = np.random.normal(28, 3, n)
battery_charge = np.random.uniform(20, 100, n)

# Derived features
temp_rise_rate = np.random.normal(0.2, 0.1, n)  # temperature rise rate
temp_vs_ambient = temperature - ambient_temp
power = voltage * current

# Build DataFrame
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

# Smarter label logic for overheating
data['overheating'] = (
    ((temp_vs_ambient > 5) & (power > 5)) |
    (temp_rise_rate > 0.3)
).astype(int)

# Optional: make it imbalanced to reflect real-world rarity of overheating
data.loc[data.sample(frac=0.7, random_state=42).index, 'overheating'] = 0

# Show label distribution
label_distribution = data['overheating'].value_counts()

# Save to CSV
csv_path = "/mnt/data/enhanced_battery_data.csv"
data.to_csv(csv_path, index=False)

csv_path, label_distribution.head()
