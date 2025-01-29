import streamlit as st
import pandas as pd
import joblib
import numpy as np
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier
from sklearn.multioutput import MultiOutputClassifier
import base64

def set_bg_from_local(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()

    bg_css = f"""
    <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
    </style>
    """
    st.markdown(bg_css, unsafe_allow_html=True)

# Call the function with your local image
set_bg_from_local("static/image14.jpg")

st.markdown("""
    <style>

        /* Change text color to black */
        .css-1v0mbdj, .css-18e3th9, .stApp {
            color: black;
        }

        .st-emotion-cache-14553y9 p {
            word-break: break-word;
            margin: 0px;
            color: black;
            font-size: 18px; /* Adjust size as needed */
            font-weight: bold;
        }

        /* Right-align text input fields */
        .stTextInput, .stTextArea, .stNumberInput, .stSelectbox, .stSlider {
            text-align: right;
        }
        
        .stSelectbox label {
            color: black !important;
        }

        /* Change color of buttons */
        .stButton>button {
            background-color: #4CAF50;
            color: black;
        }  
        
        .st-emotion-cache-h4xjwg { 
            display: none; 
        }

        .st-emotion-cache-1cvow4s b, .st-emotion-cache-1cvow4s strong {
            font-weight: bold;
        }

        /* Optional: Change colors of sidebar and other components */
        .css-1d391kg {
            color: black;
        }

        .st-emotion-cache-1cvow4s p {
            color:black;
            font-size: 18px; /* Adjust size as needed */
            font-weight: bold;
        }

        .st-emotion-cache-1cvow4s li {
            font-size: inherit;
            color:black;
        }

        .st-emotion-cache-yw8pof {
            width: 100%;
            padding: 6rem 1rem 10rem;
            max-width: 46rem;
            height:10px;
        }

        .stButton>button {
            background-color: #4CAF50;
            color: black;
            margin-top: 27.4px;
        }

        /* Change the background color of the main area */
        
        /* Styling the form inputs */
        .stTextInput input, .stNumberInput input {
            border-radius: 8px;
            padding: 10px;
        }

        /* Styling specific labels */
        .stNumberInput label {
            color: black !important;
        }
    </style>
""", unsafe_allow_html=True)

# Load pre-trained model and label encoders
@st.cache_resource
def load_resources():
    # Replace with actual file loading for your saved model and label encoders
    xgb_model = joblib.load('pesticide_model.pkl')  # Replace with the actual model file
    le_crop = joblib.load('le_crop.pkl')  # Replace with the actual encoder file
    le_pest = joblib.load('le_pest.pkl')  # Replace with the actual encoder file
    le_pesticide = joblib.load('le_pesticide.pkl')  # Replace with the actual encoder file
    le_app_method = joblib.load('le_app_method.pkl')  # Replace with the actual encoder file
    le_dosage = joblib.load('le_dosage.pkl')  # Replace with the actual encoder file
    return xgb_model, le_crop, le_pest, le_pesticide, le_app_method, le_dosage

# Function to make predictions using the model
def predict_pesticide(crop, pest, model, le_crop, le_pest, le_pesticide, le_app_method, le_dosage):
    # Encode inputs
    crop_encoded = le_crop.transform([crop])[0]
    pest_encoded = le_pest.transform([pest])[0]

    # Create a DataFrame for prediction
    input_data = pd.DataFrame([[crop_encoded, pest_encoded]], columns=['Crop', 'Pest'])

    # Predict using the trained model
    pred = model.predict(input_data)

    # Decode the predictions
    pesticide_pred = le_pesticide.inverse_transform([pred[0, 0]])[0]
    app_method_pred = le_app_method.inverse_transform([pred[0, 1]])[0]
    dosage_pred = le_dosage.inverse_transform([pred[0, 2]])[0]

    return pesticide_pred, app_method_pred, dosage_pred

# Streamlit app UI
st.write("Enter the following values to get the pesticide recommendations:")

# Input form
with st.form("pesticide_form"):
    crop_name = st.selectbox("Select the crop:", ['Barley', 'Cotton', 'Maize', 'Peanut', 'Potato', 'Rice', 'Soybean',
       'Sugarcane', 'Tomato', 'Wheat', 'apple', 'banana', 'blackgram',
       'chickpea', 'coconut', 'coffee', 'grapes', 'jute', 'kidneybeans',
       'lentil', 'mango', 'mothbeans', 'mungbean', 'muskmelon', 'orange',
       'papaya', 'pigeonpeas', 'pomegranate', 'watermelon'])  # Add your crop list here
    pest_name = st.selectbox("Select the pest:", ['Stem Borer', 'Potato Beetle', 'Soybean Looper', 'Armyworm',
       'Whitefly', 'Peanut Bud Necrosis Virus',
       'Barley Yellow Dwarf Virus', 'Bollworm', 'Sugarcane Borer',
       'Aphids', 'Codling Moth', 'Banana Aphids', 'Thrips', 'Helicoverpa',
       'Red Palm Weevil', 'Coffee Berry Borer', 'Powdery Mildew',
       'Jute Stem Weevil', 'Cutworm', 'Mango Hopper', 'Pod Borer',
       'Citrus Psylla', 'Mealybug', 'Maruca Pod Borer', 'Leaf Miner'])  # Add pest names here

    # Submit button
    submitted = st.form_submit_button("Predict Pesticide")

# When the form is submitted
if submitted:
    try:
        # Load model and encoders
        xgb_model, le_crop, le_pest, le_pesticide, le_app_method, le_dosage = load_resources()

        # Get predictions
        pesticide, app_method, dosage = predict_pesticide(
            crop_name, pest_name, xgb_model, le_crop, le_pest, le_pesticide, le_app_method, le_dosage
        )

        # Display results
        st.write(f"Predicted Pesticide: {pesticide}")
        st.write(f"Application Method: {app_method}")
        st.write(f"Dosage: {dosage}")

    except Exception as e:
        st.error(f"An error occurred: {e}")