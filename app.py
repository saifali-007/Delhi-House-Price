# import streamlit as st
# import pandas as pd
# import pickle



# # Load pipeline (preprocessing + model)
# model = pickle.load(open("delhi_price_model.pkl", "rb"))

# st.title("🏠 Delhi House Price Prediction")

# # Categorial values
# mapping_furnishing = {"Furnished": 2, "Semi-Furnished": 1, "Unfurnished": 0}
# mapping_parking = {"Yes": 1, "No": 0}
# mapping_status = {"Ready to move": 1, "Under construction": 0}
# mapping_location = {
#     'Dwarka': 0, 
#     'Saket': 1, 
#     'Rohini': 2, 
#     'Lajpat Nagar': 3, 
#     'Vasant Kunj': 4, 
#     'Karol Bagh': 5
# }

# # Input fields


# BHK = st.number_input("Number of BHK", min_value=1, max_value=10, step=1)
# localities = ["Dwarka", "Saket", "Rohini", "Lajpat Nagar", "Vasant Kunj", "Karol Bagh"]
# Location = st.selectbox("Select Location", localities)
# Bathroom = st.number_input("Number of Bathrooms", min_value=1, max_value=10, step=1)
# furnishing = st.selectbox("Furnishing", ["Furnished", "Semi-Furnished", "Unfurnished"])
# parking = st.selectbox("Parking", ["Yes", "No"])
# Area_yards = st.number_input("Enter Area (sq ft)", min_value=100, max_value=10000, step=50)
# status = st.selectbox("Status", ["Ready to move", "Under construction"])


# if st.button("Predict Price"):
#     # Prepare input
#     input_df = pd.DataFrame({
#         "BHK": [BHK],
#         "Location": [mapping_location[Location]],
#         "Bathroom": [Bathroom],
#         "Furnishing":[mapping_furnishing[furnishing]],
#         # "Parking": [parking],
#         "Parking": [mapping_parking[parking]],
#         "Area_Yards": [Area_yards],
#         "Status" : [mapping_status[status]]
        
#     })
    
#     # Predict
#     prediction = model.predict(input_df)[0]
    
#     st.success(f"🏡 Estimated House Price: ₹ {round(prediction, 2)} Lakhs")


import streamlit as st
import pandas as pd
import pickle
import numpy as np

# --- Denormalization Constants (Derived from the original dataset) ---
# The model predicts a value scaled between 0 and 1.
# Original Minimum Price (INR): 1,000,000
# Original Maximum Price (INR): 93,000,000
MIN_PRICE = 1000000
MAX_PRICE = 93000000
PRICE_RANGE = MAX_PRICE - MIN_PRICE
# -------------------------------------------------------------------

# Load pipeline (preprocessing + model)
try:
    model = pickle.load(open("delhi_price_model.pkl", "rb"))
except FileNotFoundError:
    st.error("Error: Model file 'delhi_price_model.pkl' not found. Please ensure the model is saved correctly.")
    st.stop()


st.title("🏠 Delhi House Price Prediction")

# Categorial values mappings (Used for model input)
mapping_furnishing = {"Furnished": 2, "Semi-Furnished": 1, "Unfurnished": 0}
mapping_parking = {"Yes": 1, "No": 0}
mapping_status = {"Ready to move": 1, "Under construction": 0}
mapping_location = {
    'Dwarka': 0, 
    'Saket': 1, 
    'Rohini': 2, 
    'Lajpat Nagar': 3, 
    'Vasant Kunj': 4, 
    'Karol Bagh': 5
}

# Input fields
BHK = st.number_input("Number of BHK", min_value=1, max_value=10, step=1)
localities = ["Dwarka", "Saket", "Rohini", "Lajpat Nagar", "Vasant Kunj", "Karol Bagh"]
Locality = st.selectbox("Select Location", localities)
Bathroom = st.number_input("Number of Bathrooms", min_value=1, max_value=10, step=1)
furnishing = st.selectbox("Furnishing", ["Furnished", "Semi-Furnished", "Unfurnished"])
parking = st.selectbox("Parking", ["Yes", "No"])
Area_yards = st.number_input("Enter Area (sq ft)", min_value=100, max_value=10000, step=50)
status = st.selectbox("Status", ["Ready to move", "Under construction"])


if st.button("Predict Price"):
    try:
        # Prepare input DataFrame (Features must match the model's training features/order)
        input_df = pd.DataFrame({
            "BHK": [BHK],
            "Area_Yards": [Area_yards],
            "Location": [mapping_location[Locality]],
            "Bathroom": [Bathroom],
            "Furnishing":[mapping_furnishing[furnishing]],
            "Parking": [mapping_parking[parking]],
            "Status" : [mapping_status[status]]
        })
        
        # 1. Predict the Normalized Price (a value between 0 and 1)
        normalized_prediction = model.predict(input_df)[0]
        
        # 2. Denormalize the Price back to INR (using the Min/Max from the dataset)
        actual_price_in_inr = (normalized_prediction * PRICE_RANGE) + MIN_PRICE
        
        # 3. Convert to Lakhs for better readability (1 Lakh = 100,000 INR)
        price_in_lakhs = actual_price_in_inr / 100000
        
        st.success(f"🏡 Estimated House Price: ₹ {price_in_lakhs:,.2f} Lakhs")
        st.info(f"Raw Normalized Prediction: {normalized_prediction:.4f}")

    except Exception as e:
        st.error(f"An error occurred during prediction: {e}")
