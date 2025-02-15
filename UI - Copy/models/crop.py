# Import Libraries
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

# Importing Data
crop = pd.read_csv(r"C:\Users\himan\OneDrive\Desktop\gopu2408\UI\data\Crop_recommendation.csv")

# Display dataset information
print("Dataset Head:")
print(crop.head())

print("\nDataset Shape:")
print(crop.shape)

print("\nDataset Info:")
print(crop.info())

print("\nChecking for null values:")
print(crop.isnull().sum())

print("\nChecking for duplicate rows:")
print(crop.duplicated().sum())

print("\nDataset Description:")
print(crop.describe())

print("\nLabel Value Counts:")
print(crop['label'].value_counts())

# Encoding target variable
crop_dict = {
    'rice': 1, 'maize': 2, 'jute': 3, 'cotton': 4, 'coconut': 5, 'papaya': 6, 
    'orange': 7, 'apple': 8, 'muskmelon': 9, 'watermelon': 10, 'grapes': 11, 
    'mango': 12, 'banana': 13, 'pomegranate': 14, 'lentil': 15, 'blackgram': 16, 
    'mungbean': 17, 'mothbeans': 18, 'pigeonpeas': 19, 'kidneybeans': 20, 
    'chickpea': 21, 'coffee': 22, 'wheat': 23
}
crop['crop_num'] = crop['label'].map(crop_dict)

print("\nDataset after encoding:")
print(crop.head())

# Splitting dataset into features and target
X = crop[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]  # Features
y = crop['crop_num']  # Target

# Splitting into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize a dictionary to store model results
model_results = {}

# 1. Random Forest Classifier
rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X_train, y_train)
rf_y_pred = rf_model.predict(X_test)
rf_accuracy = accuracy_score(y_test, rf_y_pred)
model_results['Random Forest'] = rf_accuracy

# 2. Decision Tree Classifier
dt_model = DecisionTreeClassifier(random_state=42)
dt_model.fit(X_train, y_train)
dt_y_pred = dt_model.predict(X_test)
dt_accuracy = accuracy_score(y_test, dt_y_pred)
model_results['Decision Tree'] = dt_accuracy

# 3. Support Vector Classifier (SVC)
svc_model = SVC(kernel='linear', random_state=42)
svc_model.fit(X_train, y_train)
svc_y_pred = svc_model.predict(X_test)
svc_accuracy = accuracy_score(y_test, svc_y_pred)
model_results['SVC (Linear Kernel)'] = svc_accuracy

# Print accuracy for all models
print("\nModel Performance:")
for model, accuracy in model_results.items():
    print(f"{model}: {accuracy:.2f}")

# Store predictions for each model
predictions = {
    'Random Forest': rf_y_pred,
    'Decision Tree': dt_y_pred,
    'SVC (Linear Kernel)': svc_y_pred
}

# Find the model with the highest accuracy
best_model = max(model_results, key=model_results.get)
best_model_predictions = predictions[best_model]

# Print classification report and confusion matrix for the best model
print(f"\nBest Model: {best_model}")
print("Classification Report:")
print(classification_report(y_test, best_model_predictions))
print("Confusion Matrix:")
print(confusion_matrix(y_test, best_model_predictions))


# Save the trained model (Random Forest)
joblib.dump(rf_model, 'crop_recommendation_model.pkl')