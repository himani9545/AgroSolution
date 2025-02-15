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
            margin:0;
            padding:0;
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
        .st-emotion-cache-ul70r3 p {
    word-break: break-word;
    color: black;
}
            .st-emotion-cache-1cvow4s h1 {
        font-size: 2.5rem;
        font-weight: 700;
        padding: 1.25rem 0px 1rem;
    }
.st-emotion-cache-1jzia57 h1, .st-emotion-cache-1jzia57 h2, .st-emotion-cache-1jzia57 h3, .st-emotion-cache-1jzia57 h4, .st-emotion-cache-1jzia57 h5, .st-emotion-cache-1jzia57 h6, .st-emotion-cache-1jzia57 span {
    scroll-margin-top: 3.75rem;
    color: black;
}

.st-emotion-cache-1tpl0xr p {
    font-weight: bold;
    word-break: break-word;
    margin-bottom: 0px;
    font-size: 14px;
    color: black;
}

.st-d4 {
    opacity: 1;
    color: black;
    font-weight: bold;
}


        /* Change the background color of the main area */
        

        /* Styling the form inputs */
        .stTextInput input, .stNumberInput input {
            border-radius: 8px;
            padding: 10px;
        }
        .st-emotion-cache-b0y9n5 {
    display: inline-flex
;
    -webkit-box-align: center;
    align-items: center;
    -webkit-box-pack: center;
    justify-content: center;
    font-weight: 400;
    padding: 0.25rem 0.75rem;
    border-radius: 0.5rem;
    min-height: 2.5rem;
    margin: 0px;
    line-height: 1.6;
    text-transform: none;
    font-size: inherit;
    font-family: inherit;
    color: inherit; 
    width: auto;
    cursor: pointer;
    user-select: none;
    background-color: green;
    border: 1px solid rgba(250, 250, 250, 0.2);
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
    le_disease = joblib.load('le_disease.pkl')
    le_pesticide = joblib.load('le_pesticide.pkl')  # Replace with the actual encoder file
    le_app_method = joblib.load('le_app_method.pkl')  # Replace with the actual encoder file
    le_dosage = joblib.load('le_dosage.pkl')  # Replace with the actual encoder file
    return xgb_model, le_crop, le_pest,le_disease, le_pesticide, le_app_method, le_dosage

# Crop-specific pests and diseases dictionary
crop_data = {
    "Barley": {"pests": [ 'Whitefly', 'Looper', 'Bud Necrosis Virus', 'Barley Yellow Dwarf Virus', 'Stem Borer', 'Armyworm', 'Aphids', 'Bollworm']
, "diseases": ['Leaf Spot', 'Leaf Blight', 'Defoliation & Wilting', 'Stem Rot', ' Bud Necrosis Disease', 'Yellow Mosaic Disease', 'Barley Yellow Dwarf Disease']
},
    "Cotton": {"pests": ['Potato Beetle', 'Whitefly', 'Soybean Looper', 'Peanut Bud Necrosis Virus', 'Barley Yellow Dwarf Virus', 'Stem Borer', 'Armyworm', 'Aphids', 'Sugarcane Borer', 'Bollworm'],
     "diseases": ['Leaf Blight', 'Leaf Spot', 'Defoliation & Wilting', 'Stem Rot', 'Yellow Mosaic Disease']
},
    "Maize": {"pests": ['Whitefly', 'Potato Beetle', 'Soybean Looper', 'Peanut Bud Necrosis Virus', 'Barley Yellow Dwarf Virus', 'Stem Borer', 'Armyworm', 'Aphids', 'Sugarcane Borer', 'Bollworm']
, "diseases": ['Leaf Blight', 'Leaf Spot', 'Defoliation & Wilting', 'Stem Rot', 'Yellow Mosaic Disease']
},
    "Peanut": {"pests":['Potato Beetle', 'Whitefly', 'Soybean Looper', 'Peanut Bud Necrosis Virus', 'Stem Borer', 'Armyworm', 'Aphids', 'Sugarcane Borer', 'Bollworm']
, "diseases": [ 'Leaf Spot', 'Leaf Blight', 'Defoliation & Wilting', 'Stem Rot', 'Yellow Mosaic Disease']
},
 "Potato": {"pests":['Potato Beetle', 'Whitefly', 'Soybean Looper', 'Peanut Bud Necrosis Virus', 'Stem Borer', 'Armyworm', 'Aphids', 'Sugarcane Borer', 'Bollworm']
, "diseases": [ 'Leaf Spot', 'Leaf Blight', 'Defoliation & Wilting', 'Stem Rot', 'Yellow Mosaic Disease']
},
 "Rice": {"pests":['Potato Beetle', 'Whitefly', 'Soybean Looper', 'Peanut Bud Necrosis Virus', 'Stem Borer', 'Armyworm', 'Aphids', 'Sugarcane Borer', 'Bollworm']
, "diseases": [ 'Leaf Spot', 'Leaf Blight', 'Defoliation & Wilting', 'Stem Rot', 'Yellow Mosaic Disease']
},
 "Soyabean": {"pests":['Potato Beetle', 'Whitefly', 'Soybean Looper', 'Peanut Bud Necrosis Virus', 'Stem Borer', 'Armyworm', 'Aphids', 'Sugarcane Borer', 'Bollworm']
, "diseases": [ 'Leaf Spot', 'Leaf Blight', 'Defoliation & Wilting', 'Stem Rot', 'Yellow Mosaic Disease']
},
"Sugarcane": {"pests":['Potato Beetle', 'Whitefly', 'Soybean Looper', 'Peanut Bud Necrosis Virus', 'Stem Borer', 'Armyworm', 'Aphids', 'Sugarcane Borer', 'Bollworm']
, "diseases": ['Leaf Spot', 'Leaf Blight', 'Defoliation & Wilting', 'Stem Rot', 'Yellow Mosaic Disease']
},
"Tomato": {"pests":['Potato Beetle', 'Whitefly', 'Soybean Looper', 'Peanut Bud Necrosis Virus', 'Stem Borer', 'Armyworm', 'Aphids', 'Sugarcane Borer', 'Bollworm']
, "diseases": [ 'Leaf Spot', 'Leaf Blight', 'Defoliation & Wilting', 'Stem Rot', 'Yellow Mosaic Disease']
},
"Wheat": {"pests":['Potato Beetle', 'Whitefly', 'Soybean Looper', 'Peanut Bud Necrosis Virus', 'Stem Borer', 'Armyworm', 'Aphids', 'Sugarcane Borer', 'Bollworm']
, "diseases": [ 'Leaf Spot', 'Leaf Blight', 'Defoliation & Wilting', 'Stem Rot', 'Yellow Mosaic Disease']
},
"Apple": {"pests":['Codling Moth']
, "diseases": ['General Crop Damage']
},
"Banana": {"pests":['Banana Aphids']
, "diseases": ['General Crop Damage']
},
"coconut": {"pests":['Red Palm Weevil']
, "diseases": ['General Crop Damage']
},
"Blackgram": {"pests":['Thrips']
, "diseases": ['Tobacco Streak Virus']
},
"Chickpea": {"pests":['Helicoverpa']
, "diseases": ['General Crop Damage']
},
"Coffee": {"pests":['Coffee Berry Borer']
, "diseases": ['General Crop Damage']
},
"grapes": {"pests":['Powdery Mildew']
, "diseases": ['Leaf Blight']
},
"jute": {"pests":['Jute Stem Weevil']
, "diseases": ['General Crop Damage']
},
"kidneybeans": {"pests":['Whitefly']
, "diseases": ['Yellow Mosaic Disease']
},
"lentil": {"pests":['Cutworm']
, "diseases": ['General Crop Damage']
},
"mango": {"pests":['Mango Hopper']
, "diseases": ['General Crop Damage']
},
"mothbeans": {"pests":['Aphids']
, "diseases": ['General Crop Damage']
},
"mungbean": {"pests":['Pod Borer']
, "diseases": ['General Crop Damage']
},
"muskmelon": {"pests":['Aphids']
, "diseases": ['General Crop Damage']
},
"orange": {"pests":['Citrus Psylla']
, "diseases": ['General Crop Damage']
},
"papaya": {"pests":['Mealybug']
, "diseases": ['Sooty Mold']
},
"pigeonpeas": {"pests":['Maruca Pod Borer']
, "diseases": ['General Crop Damage']
},
"pomegranate": {"pests":['Thrips']
, "diseases": ['Tobacco Streak Virus']
},
"watermelon": {"pests":['Leaf Miner']
, "diseases": ['General Crop Damage']
},
}

# Function to make predictions
def predict_pesticide(crop, pest, disease, model, le_crop, le_pest, le_disease, le_pesticide, le_app_method, le_dosage):
    input_data = pd.DataFrame([[
        le_crop.transform([crop])[0],
        le_pest.transform([pest])[0],
        le_disease.transform([disease])[0]
    ]], columns=['Crop', 'Pest', 'Disease'])
    
    pred = model.predict(input_data)
    return (
        le_pesticide.inverse_transform([pred[0, 0]])[0],
        le_app_method.inverse_transform([pred[0, 1]])[0],
        le_dosage.inverse_transform([pred[0, 2]])[0]
    )

# Streamlit UI
st.title("Pesticide Recommendation System")

# Select Crop
selected_crop = st.selectbox("Select Crop:", list(crop_data.keys()))

# Filter pests and diseases dynamically
pest_options = crop_data[selected_crop]["pests"]
disease_options = crop_data[selected_crop]["diseases"]

selected_pest = st.selectbox("Select Pest:", pest_options)
selected_disease = st.selectbox("Select Disease:", disease_options)

if st.button("Predict Pesticide"):
    try:
        # Load model & encoders
        model, le_crop, le_pest, le_disease, le_pesticide, le_app_method, le_dosage = load_resources()
        
        # Get prediction
        pesticide, app_method, dosage = predict_pesticide(
            selected_crop, selected_pest, selected_disease,
            model, le_crop, le_pest, le_disease, le_pesticide, le_app_method, le_dosage
        )
        
        # Display Results
        st.success(f"Predicted Pesticide: {pesticide}")
        st.write(f"Application Method: {app_method}")
        st.write(f"Dosage: {dosage}")
    except Exception as e:
        st.error(f"Error: {e}")