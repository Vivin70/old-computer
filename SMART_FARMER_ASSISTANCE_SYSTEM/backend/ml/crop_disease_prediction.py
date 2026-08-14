import pandas as pd
from sklearn.naive_bayes import GaussianNB
import pickle

# Sample dataset
data = {
    'yellow_leaves': [1,0,1,0,1,0,1,0],
    'brown_spots': [1,1,0,0,1,0,0,0],
    'wilting': [0,1,1,0,1,0,1,0],
    'disease': [
        'Leaf Blight',
        'Bacterial Wilt',
        'Leaf Blight',
        'Healthy',
        'Leaf Blight',
        'Healthy',
        'Bacterial Wilt',
        'Healthy'
    ]
}

df = pd.DataFrame(data)

X = df[['yellow_leaves', 'brown_spots', 'wilting']]
y = df['disease']

model = GaussianNB()
model.fit(X, y)

# Save model
pickle.dump(model, open('backend/ml/crop_disease_model.pkl', 'wb'))

print("Crop disease model trained & saved")
