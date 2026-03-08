import pandas as pd
import numpy as np
import pickle
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, VotingRegressor
from sklearn.metrics import r2_score
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBRegressor

# ---------------- CREATE MODELS FOLDER ---------------- #
if not os.path.exists("models"):
    os.makedirs("models")

# ---------------- LOAD DATA ---------------- #
data = pd.read_csv("dataset/Salary Data.csv")

print("Dataset Loaded Successfully")
print("Columns:", data.columns)

# ---------------- CLEAN DATA ---------------- #
data = data.dropna()   # Remove missing values

# ---------------- ENCODING ---------------- #
le_gender = LabelEncoder()
le_edu = LabelEncoder()
le_job = LabelEncoder()

data["Gender"] = le_gender.fit_transform(data["Gender"])
data["Education Level"] = le_edu.fit_transform(data["Education Level"])
data["Job Title"] = le_job.fit_transform(data["Job Title"])

# Save encoders
pickle.dump(le_gender, open("models/gender_encoder.pkl", "wb"))
pickle.dump(le_edu, open("models/edu_encoder.pkl", "wb"))
pickle.dump(le_job, open("models/job_encoder.pkl", "wb"))

# ---------------- FEATURES & TARGET ---------------- #
X = data[["Age", "Gender", "Education Level", "Job Title", "Years of Experience"]]
y = data["Salary"]

# ---------------- TRAIN TEST SPLIT ---------------- #
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ---------------- MODELS ---------------- #
rf = RandomForestRegressor(n_estimators=100, random_state=42)
gb = GradientBoostingRegressor(n_estimators=100, random_state=42)
xgb = XGBRegressor(n_estimators=100, random_state=42, verbosity=0)

# ---------------- ENSEMBLE ---------------- #
ensemble = VotingRegressor([
    ("rf", rf),
    ("gb", gb),
    ("xgb", xgb)
])

# ---------------- TRAIN MODEL ---------------- #
ensemble.fit(X_train, y_train)

# ---------------- EVALUATE ---------------- #
y_pred = ensemble.predict(X_test)
r2 = r2_score(y_test, y_pred)

print("Model R2 Score:", round(r2, 4))

# ---------------- FEATURE IMPORTANCE ---------------- #
rf.fit(X_train, y_train)
importance = rf.feature_importances_

importance_dict = {
    "Age": importance[0],
    "Gender": importance[1],
    "Education Level": importance[2],
    "Job Title": importance[3],
    "Years of Experience": importance[4]
}

print("Feature Importance:", importance_dict)

pickle.dump(importance_dict, open("models/feature_importance.pkl", "wb"))

# ---------------- SAVE MODEL ---------------- #
pickle.dump(ensemble, open("models/salary_model.pkl", "wb"))

print("\n✅ Model Training Complete!")
print("✅ Model saved in models/salary_model.pkl")
print("✅ Encoders saved")