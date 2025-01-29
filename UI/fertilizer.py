#importing libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import warnings
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

# Suppress warnings
warnings.filterwarnings('ignore')

# Importing the dataset
data = pd.read_csv(r"C:\Users\himan\OneDrive\Desktop\gopu2408\UI\expanded_fertilizer_dataset.csv")
print(data.head())

# Display value counts for 'Recommended Fertilizers'
value_counts = data['Recommended Fertilizers'].value_counts()
print(value_counts)

# Dataset information
data.info()

# Map fertilizer names to unique codes
fertilizer_encoder = LabelEncoder()
data['Fertilizer_Code'] = fertilizer_encoder.fit_transform(data['Recommended Fertilizers'])
reverse_fertilizer_mapping = {index: name for index, name in enumerate(fertilizer_encoder.classes_)}

# Encode the Crop column
crop_encoder = LabelEncoder()
data['Crop_Code'] = crop_encoder.fit_transform(data['Crop'])

# Features and target variable
X = data[['Crop_Code', 'N', 'P', 'K', 'pH', 'soil_moisture']]
y = data['Fertilizer_Code']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the feature data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train a Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Evaluate the model
y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Display confusion matrix
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Map predicted Fertilizer_Code back to fertilizer names
y_test_names = [reverse_fertilizer_mapping[code] for code in y_test]
y_pred_names = [reverse_fertilizer_mapping[code] for code in y_pred]

# Display predictions with fertilizer names
output_df = X_test.copy()
output_df['Actual Fertilizer'] = y_test_names
output_df['Predicted Fertilizer'] = y_pred_names

# Function for testing with user input
def predict_fertilizer(crop_name, n, p, k, ph, soil_moisture):
    # Encode the crop name
    crop_code = crop_encoder.transform([crop_name])[0]
    # Create a DataFrame for the input values
    input_data = pd.DataFrame([[crop_code, n, p, k, ph, soil_moisture]], 
                              columns=['Crop_Code', 'N', 'P', 'K', 'pH', 'soil_moisture'])
    # Scale the input data
    input_scaled = scaler.transform(input_data)
    # Predict fertilizer code
    predicted_code = model.predict(input_scaled)[0]
    # Get fertilizer name from the code
    fertilizer_name = reverse_fertilizer_mapping[predicted_code]
    return fertilizer_name

# Example of testing with your own values
print("\nTest with Custom Input:")
custom_crop = "coconut"  # Replace with a valid crop name from your dataset
custom_n = 20
custom_p = 10
custom_k = 30
custom_ph = 5
custom_soil_moisture = 45
predicted_fertilizer = predict_fertilizer(custom_crop, custom_n, custom_p, custom_k, custom_ph, custom_soil_moisture)
print(f"Predicted Fertilizer for Crop={custom_crop}, N={custom_n}, P={custom_p}, K={custom_k}, pH={custom_ph}, Soil Moisture={custom_soil_moisture}: {predicted_fertilizer}")

# Save models and encoders
joblib.dump(model, 'fertilizer_recommendation_model.pkl')
joblib.dump(fertilizer_encoder, 'fertilizer_label_encoder.pkl')
joblib.dump(crop_encoder, 'crop_label_encoder.pkl')
joblib.dump(scaler, 'scaler.pkl')

print("Model and encoders saved successfully!")
