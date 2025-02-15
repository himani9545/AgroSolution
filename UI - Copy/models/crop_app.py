import streamlit as st
import joblib
import numpy as np
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
set_bg_from_local(r"C:\Users\himan\OneDrive\Desktop\gopu2408\UI\static\images\image14.jpg")

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

# Load the trained model
model = joblib.load('crop_recommendation_model.pkl')

# Mapping crop names to crop numbers
crop_name_mapping = {
    'rice': 1,
    'maize': 2,
    'jute': 3,
    'cotton': 4,
    'coconut': 5,
    'papaya': 6,
    'orange': 7,
    'apple': 8,
    'muskmelon': 9,
    'watermelon': 10,
    'grapes': 11,
    'mango': 12,
    'banana': 13,
    'pomegranate': 14,
    'lentil': 15,
    'blackgram': 16,
    'mungbean': 17,
    'mothbeans': 18,
    'pigeonpeas': 19,
    'kidneybeans': 20,
    'chickpea': 21,
    'coffee': 22,
    'wheat':23
}

# Reverse mapping from crop number to crop name
st.markdown(
    "<h2 style='text-align: center; font-weight: bold;color: black'>Crop Recommendation System:</h2>", 
    unsafe_allow_html=True
)

crop_num_mapping = {v: k for k, v in crop_name_mapping.items()}
st.write('Enter the following values to get the crop recommendations:')

# Create columns for side-by-side text fields
col1, col2 = st.columns(2)

# Collect user inputs for the features, placing them in columns
with col1:
    N = st.number_input("Enter Nitrogen (N):", min_value=0.0)
    P = st.number_input("Enter Phosphorus (P):", min_value=0.0)
    K = st.number_input("Enter Potassium (K):", min_value=0.0)
    temperature = st.number_input("Enter Temperature (in Celsius):", min_value=0.0)

with col2:
    humidity = st.number_input("Enter Humidity (in percentage):", min_value=0.0, max_value=100.0)
    ph = st.number_input("Enter pH:", min_value=0.0)
    rainfall = st.number_input("Enter Rainfall (in mm):", min_value=0.0)
    predict_button = st.button("Predict Crops")
# Create an input array for the model
user_input = np.array([N, P, K, temperature, humidity, ph, rainfall]).reshape(1, -1)

# Button to make the prediction
if predict_button:
    # Predict probabilities for all crops
    crop_probabilities = model.predict_proba(user_input)[0]  # Get probabilities for each crop
    
    # Get the indices of the top 3 crops with the highest probabilities
    top_indices = crop_probabilities.argsort()[-3:][::-1]
    
    # Map the indices to crop names and probabilities
    top_crops = [(crop_num_mapping[idx + 1], crop_probabilities[idx]) for idx in top_indices]
    
    # Display the results
    st.write("The top recommended crops are:")
    for crop_name, probability in top_crops:
        st.write(f"- **{crop_name}** (Probability: {probability:.2%})")
