import streamlit as st
import pandas as pd
import pickle



# Load pipeline (preprocessing + model)
model = pickle.load(open("delhi_price_model.pkl", "rb"))

st.title("🏠 Delhi House Price Prediction")

# Categorial values
mapping_furnishing = {"Furnished": 2, "Semi-Furnished": 1, "Unfurnished": 0}
mapping_parking = {"Yes": 1, "No": 0}
mapping_status = {"Ready to move": 1, "Under construction": 0}

# Input fields


BHK = st.number_input("Number of BHK", min_value=1, max_value=10, step=1)
# Location = st.number_input("Enter Location", min_value=100, max_value=10000, step=50)
localities = ["Dwarka", "Saket", "Rohini", "Lajpat Nagar", "Vasant Kunj", "Karol Bagh"]
Location = st.selectbox("Select Location", localities)
Bathroom = st.number_input("Number of Bathrooms", min_value=1, max_value=10, step=1)
furnishing = st.selectbox("Furnishing", ["Furnished", "Semi-Furnished", "Unfurnished"])
parking = st.selectbox("Parking", ["Yes", "No"])
Area_yards = st.number_input("Enter Area (sq ft)", min_value=100, max_value=10000, step=50)
status = st.selectbox("Status", ["Ready to move", "Under construction"])


if st.button("Predict Price"):
    # Prepare input
    input_df = pd.DataFrame({
        "BHK": [BHK],
        "Location": [Location],
        "Bathroom": [Bathroom],
        "Furnishing":[mapping_furnishing[furnishing]],
        # "Parking": [parking],
        "Parking": [mapping_parking[parking]],
        "Area_Yards": [Area_yards],
        "Status" : [mapping_status[status]]
        
    })
    
    # Predict
    prediction = model.predict(input_df)[0]
    
    st.success(f"🏡 Estimated House Price: ₹ {round(prediction, 2)} Lakhs")