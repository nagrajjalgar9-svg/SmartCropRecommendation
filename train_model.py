import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

data = pd.read_csv("crop.csv")

X = data.drop("Crop Name", axis=1)
y = data["Crop Name"]

model = RandomForestClassifier(n_estimators=10)

model.fit(X, y)

joblib.dump(model, "crop_model.pkl")

print("Model trained and saved successfully!")