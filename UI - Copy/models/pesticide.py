import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier
from sklearn.multioutput import MultiOutputClassifier
import joblib

# Load dataset
data = pd.read_csv(r"C:\Users\himan\OneDrive\Desktop\gopu2408\UI\pesticide_recommendation_large.csv")

# Display initial dataset information
print(data.head())
print(data.info())

# Check unique value counts for specific columns
print(data['Crop'].value_counts())
print(data['Application Method'].value_counts())

# Initialize label encoders for categorical columns
le_crop = LabelEncoder()
le_pest = LabelEncoder()
le_pesticide = LabelEncoder()
le_app_method = LabelEncoder()
le_dosage = LabelEncoder()

# Encode the categorical data
data['Crop'] = le_crop.fit_transform(data['Crop'])
data['Pest'] = le_pest.fit_transform(data['Pest'])
data['Pesticide'] = le_pesticide.fit_transform(data['Pesticide'])
data['Application Method'] = le_app_method.fit_transform(data['Application Method'])
data['Dosage'] = le_dosage.fit_transform(data['Dosage'])

# Features and targets
X = data[['Crop', 'Pest']]
y = data[['Pesticide', 'Application Method', 'Dosage']]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the MultiOutput model with XGBClassifier
xgb_model = MultiOutputClassifier(XGBClassifier(random_state=42))
xgb_model.fit(X_train, y_train)

# Predict on the test set
y_pred = xgb_model.predict(X_test)

# Calculate Subset Accuracy
subset_accuracy = (y_pred == y_test).all(axis=1).mean()
print(f"Subset Accuracy: {subset_accuracy:.2%}")

# Calculate accuracy for each output
accuracy_pesticide = accuracy_score(y_test['Pesticide'], y_pred[:, 0])
accuracy_app_method = accuracy_score(y_test['Application Method'], y_pred[:, 1])
accuracy_dosage = accuracy_score(y_test['Dosage'], y_pred[:, 2])

print(f"Pesticide Accuracy: {accuracy_pesticide:.2%}")
print(f"Application Method Accuracy: {accuracy_app_method:.2%}")
print(f"Dosage Accuracy: {accuracy_dosage:.2%}")

# Function for user input predictions
def predict_pest_control(crop, pest):
    # Encode user inputs
    crop_encoded = le_crop.transform([crop])[0]
    pest_encoded = le_pest.transform([pest])[0]

    # Prepare input for prediction
    input_data = pd.DataFrame([[crop_encoded, pest_encoded]], columns=['Crop', 'Pest'])

    # Predict using the trained model
    pred = xgb_model.predict(input_data)

    # Decode predictions
    pesticide_pred = le_pesticide.inverse_transform([pred[0, 0]])[0]
    app_method_pred = le_app_method.inverse_transform([pred[0, 1]])[0]
    dosage_pred = le_dosage.inverse_transform([pred[0, 2]])[0]

    # Print predictions
    print(f"Predicted Pesticide: {pesticide_pred}")
    print(f"Predicted Application Method: {app_method_pred}")
    print(f"Predicted Dosage: {dosage_pred}")

# Example user input
crop_input = "pigeonpeas"
pest_input = "Maruca Pod Borer"

print(f"Input Crop: {crop_input}, Input Pest: {pest_input}")
predict_pest_control(crop_input, pest_input)

# Save the model and encoders using joblib
joblib.dump(xgb_model, 'pesticide_model.pkl')
joblib.dump(le_crop, 'le_crop.pkl')
joblib.dump(le_pest, 'le_pest.pkl')
joblib.dump(le_pesticide, 'le_pesticide.pkl')
joblib.dump(le_app_method, 'le_app_method.pkl')
joblib.dump(le_dosage, 'le_dosage.pkl')

print("Model and encoders saved using joblib!")
