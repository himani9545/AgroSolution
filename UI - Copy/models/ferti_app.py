import streamlit as st
import pandas as pd
import joblib
import numpy as np
import base64

# Function to set background image
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
    
st.markdown("""
    <style>

        /* Change text color to black */
        .css-1v0mbdj, .css-18e3th9, .stApp {
            color: black;
        }

.st-emotion-cache-1tpl0xr p {
    word-break: break-word;
    margin-bottom: 0px;
    font-size: 14px;
    color: black;
    font-weight: bold;
}

.st-emotion-cache-ul70r3 p {
    word-break: break-word;
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
# Set background image
set_bg_from_local(r"C:\Users\himan\OneDrive\Desktop\gopu2408\UI\static\images\image14.jpg")

# Load models and encoders
fertilizer_model = joblib.load('fertilizer_recommendation_model.pkl')
dosage_model = joblib.load('fertilizer_dosage_model.pkl')
fertilizer_encoder = joblib.load('fertilizer_label_encoder.pkl')
crop_encoder = joblib.load('crop_label_encoder.pkl')
scaler = joblib.load('scaler.pkl')

# Reverse mapping for fertilizer names
reverse_fertilizer_mapping = {index: name for index, name in enumerate(fertilizer_encoder.classes_)}

# Title
st.markdown(
    "<h2 style='text-align: center; font-weight: bold;color: black'>Fertilizer Recommendation System:</h2>", 
    unsafe_allow_html=True
)
st.write("Enter the following values to get the fertilizer recommendations:")

col1, col2 = st.columns(2)

# Input fields
with col1:
    crop_name = st.selectbox("Select the crop:", crop_encoder.classes_)
    n = st.number_input("Enter the Nitrogen content (N):", min_value=0, step=1)
    p = st.number_input("Enter the Phosphorus content (P):", min_value=0, step=1)
   
with col2:   
    k = st.number_input("Enter the Potassium content (K):", min_value=0, step=1)
    ph = st.number_input("Enter the pH value of the soil:", min_value=0.0, max_value=14.0, step=0.1)
    soil_moisture = st.number_input("Enter the soil moisture percentage:", min_value=0.0, max_value=100.0, step=0.1)

submitted = st.button("Predict Fertilizer and Dosage")

# Prediction logic
if submitted:
    try:
        # Encode crop
        crop_code = crop_encoder.transform([crop_name])[0]

        # Prepare input
        input_data = pd.DataFrame([[crop_code, n, p, k, ph, soil_moisture]],
                                  columns=['Crop_Code', 'N', 'P', 'K', 'pH', 'soil_moisture'])

        # Scale input
        input_scaled = scaler.transform(input_data)

        # Predict fertilizer type
        fertilizer_code = fertilizer_model.predict(input_scaled)[0]
        fertilizer_name = reverse_fertilizer_mapping[fertilizer_code]

        # Predict dosage
        predicted_dosage = dosage_model.predict(input_scaled)[0]

        # Display results
        st.success(f"**Recommended Fertilizer:** {fertilizer_name}")
        st.info(f"**Recommended Dosage:** {predicted_dosage:.2f} kg/ha")

    except Exception as e:
        st.error(f"An error occurred: {e}")
