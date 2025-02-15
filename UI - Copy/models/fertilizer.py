#importing libraries
import pandas as pd
import numpy as np
import warnings
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, classification_report, mean_absolute_error
import joblib

# Suppress warnings
warnings.filterwarnings('ignore')

# Importing the dataset
data = pd.read_csv(r"C:\Users\himan\OneDrive\Desktop\gopu2408\UI\data\updated_fertilizer_dataset.csv")  # Load the updated dataset with dosage
print(data.head())

# Encode the 'Recommended Fertilizers' column
fertilizer_encoder = LabelEncoder()
data['Fertilizer_Code'] = fertilizer_encoder.fit_transform(data['Recommended Fertilizers'])
reverse_fertilizer_mapping = {index: name for index, name in enumerate(fertilizer_encoder.classes_)}

# Encode the 'Crop' column
crop_encoder = LabelEncoder()
data['Crop_Code'] = crop_encoder.fit_transform(data['Crop'])

# Features and targets
X = data[['Crop_Code', 'N', 'P', 'K', 'pH', 'soil_moisture']]
y_fertilizer = data['Fertilizer_Code']  # Classification target
y_dosage = data['Fertilizer Dosage (kg/ha)']  # Regression target

# Split data into training and testing sets
X_train, X_test, y_train_fertilizer, y_test_fertilizer = train_test_split(X, y_fertilizer, test_size=0.2, random_state=42)
X_train, X_test, y_train_dosage, y_test_dosage = train_test_split(X, y_dosage, test_size=0.2, random_state=42)

# Standardize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train Fertilizer Type Prediction Model
fertilizer_model = RandomForestClassifier(n_estimators=100, random_state=42)
fertilizer_model.fit(X_train_scaled, y_train_fertilizer)

# Train Dosage Prediction Model
dosage_model = RandomForestRegressor(n_estimators=100, random_state=42)
dosage_model.fit(X_train_scaled, y_train_dosage)

# Evaluate Fertilizer Type Model
y_pred_fertilizer = fertilizer_model.predict(X_test_scaled)
accuracy = accuracy_score(y_test_fertilizer, y_pred_fertilizer)
print(f"Fertilizer Model Accuracy: {accuracy * 100:.2f}%")
print("\nClassification Report:")
print(classification_report(y_test_fertilizer, y_pred_fertilizer))

# Evaluate Dosage Model
y_pred_dosage = dosage_model.predict(X_test_scaled)
mae = mean_absolute_error(y_test_dosage, y_pred_dosage)
print(f"\nDosage Model MAE: {mae:.2f} kg/ha")

# Function for predicting fertilizer type and dosage
def predict_fertilizer_and_dosage(crop_name, n, p, k, ph, soil_moisture):
    # Encode crop
    crop_code = crop_encoder.transform([crop_name])[0]
    input_data = pd.DataFrame([[crop_code, n, p, k, ph, soil_moisture]], 
                              columns=['Crop_Code', 'N', 'P', 'K', 'pH', 'soil_moisture'])
    # Scale input
    input_scaled = scaler.transform(input_data)
    
    # Predict fertilizer type
    predicted_fertilizer_code = fertilizer_model.predict(input_scaled)[0]
    fertilizer_name = reverse_fertilizer_mapping[predicted_fertilizer_code]
    
    # Predict dosage
    predicted_dosage = dosage_model.predict(input_scaled)[0]
    
    return fertilizer_name, round(predicted_dosage, 2)

# Example test case
custom_crop = "rice"
custom_n, custom_p, custom_k, custom_ph, custom_soil_moisture = 80, 40, 40, 5.5, 30
predicted_fertilizer, predicted_dosage = predict_fertilizer_and_dosage(custom_crop, custom_n, custom_p, custom_k, custom_ph, custom_soil_moisture)

print(f"\nPredicted Fertilizer: {predicted_fertilizer}, Dosage: {predicted_dosage} kg/ha")

# Save models and encoders
joblib.dump(fertilizer_model, 'fertilizer_recommendation_model.pkl')
joblib.dump(dosage_model, 'fertilizer_dosage_model.pkl')
joblib.dump(fertilizer_encoder, 'fertilizer_label_encoder.pkl')
joblib.dump(crop_encoder, 'crop_label_encoder.pkl')
joblib.dump(scaler, 'scaler.pkl')

print("Models and encoders saved successfully!")
