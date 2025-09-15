import streamlit as st
import pandas as pd
import pickle

# Load pipeline (preprocessing + model)
model = pickle.load(open("delhi_price_model.pkl", "rb"))

st.title("🏠 Delhi House Price Prediction")

# Input fields
Area = st.number_input("Enter Area (sq ft)", min_value=100, max_value=10000, step=50)
BHK = st.number_input("Number of BHK", min_value=1, max_value=10, step=1)
Bathroom = st.number_input("Number of Bathrooms", min_value=1, max_value=10, step=1)
Location = st.number_input("Enter Area", min_value=100, max_value=10000, step=50)

# Dropdown for location
# location = st.selectbox(
#     "Select Location",
#     ["Delhi", "Noida", "Gurgaon", "Faridabad", "Ghaziabad", "Other"]
# )

if st.button("Predict Price"):
    # Prepare input
    input_df = pd.DataFrame({
        "Area": [Area],
        "BHK": [BHK],
        "Bathroom": [Bathroom],
        "Location": [Location]
    })
    
    # Predict
    prediction = model.predict(input_df)[0]
    
    st.success(f"🏡 Estimated House Price: ₹ {round(prediction, 2)} Lakhs")