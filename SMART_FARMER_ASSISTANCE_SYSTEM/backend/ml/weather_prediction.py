import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import pickle

# Sample dataset
data = {
    'temperature': [20, 25, 30, 35, 40, 28, 22, 18],
    'humidity': [80, 70, 60, 50, 40, 75, 85, 90],
    'rain': [1, 0, 0, 0, 0, 1, 1, 1]
}

df = pd.DataFrame(data)

X = df[['temperature', 'humidity']]
y = df['rain']

model = DecisionTreeClassifier()
model.fit(X, y)

# Save model
pickle.dump(model, open('backend/ml/weather_model.pkl', 'wb'))

print("Weather model trained and saved")
