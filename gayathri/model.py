import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

# Load dataset
data = pd.read_csv("ethereum.csv")

# Use Date index
data['Date'] = pd.to_datetime(data['Date'])
data['Days'] = (data['Date'] - data['Date'].min()).dt.days

X = data[['Days']]
y = data['Close']

# Train model
model = LinearRegression()
model.fit(X, y)

# Save model
pickle.dump(model, open("eth_model.pkl", "wb"))
print("Model trained and saved")
