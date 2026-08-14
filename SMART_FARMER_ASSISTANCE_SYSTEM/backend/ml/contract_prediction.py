import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

# Sample dataset
data = {
    'crop': [0, 0, 1, 1, 2, 2],  # 0=Rice, 1=Wheat, 2=Maize
    'quantity': [100, 200, 150, 300, 120, 250],
    'market_price': [20, 22, 25, 27, 18, 20],
    'contract_price': [2100, 4400, 3800, 8200, 2200, 5200]
}

df = pd.DataFrame(data)

X = df[['crop', 'quantity', 'market_price']]
y = df['contract_price']

model = LinearRegression()
model.fit(X, y)

pickle.dump(model, open('backend/ml/contract_model.pkl', 'wb'))

print("Contract prediction model trained & saved")
