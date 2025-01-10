import streamlit as st
import pandas as pd
import joblib
import numpy as np
import requests

# API for Exchange Rate (Using exchangerate-api.com)
EXCHANGE_RATE_API_URL = "https://api.exchangerate-api.com/v4/latest/USD"

# Load the saved model and preprocessor
try:
    model = joblib.load('vehicle_price_model.joblib')
    preprocessor = joblib.load('preprocessor.joblib')
except FileNotFoundError:
    st.error("Error: Model or preprocessor file not found. Please make sure the files 'vehicle_price_model.joblib' and 'preprocessor.joblib' are in the same directory.")
    st.stop()
except Exception as e:
    st.error(f"Error loading model or preprocessor: {e}")
    st.stop()

# Function to fetch exchange rate
def get_exchange_rate():
    """Fetches the latest ETB to USD exchange rate from the API."""
    try:
        response = requests.get(EXCHANGE_RATE_API_URL)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        etb_to_usd = data['rates']['ETB']
        return etb_to_usd
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching exchange rate: {e}")
        return None
    except KeyError:
        st.error("Error: Could not extract the exchange rate data from API response.")
        return None
    except Exception as e:
        st.error(f"Unexpected error while fetching the exchange rate: {e}")
        return None

# Load data for dropdowns
data = pd.read_csv('VehicleData2.csv')
data.dropna(subset=[' Price '], inplace=True)  # Ensure no NaN in target column
data.fillna('Unknown', inplace=True)  # Fill NaN values in other columns

# Fetch the Exchange rate
etb_to_usd_rate = get_exchange_rate()

if etb_to_usd_rate is None:
    st.error("Could not retrieve the current exchange rate. Please check your internet connection.")
    st.stop()

# UI Elements
st.title("HKTM Vehicle Price Predictor")
st.markdown("Select the car features to predict the price.")
st.write(f"Today's Exchange Rate: 1 USD = {etb_to_usd_rate:.2f} ETB")  # Display exchange rate on top

# Dropdowns
make = st.selectbox("Make", options=sorted(data['Make'].unique()))
filtered_data = data[data['Make'] == make]
filtered_models = filtered_data['Model'].unique()
model_name = st.selectbox("Model", options=sorted(filtered_models))
filtered_fuels = filtered_data[filtered_data['Model'] == model_name]['Fuel'].unique()
fuel = st.selectbox("Fuel", options=sorted(filtered_fuels))
year = st.selectbox("Year", options=sorted(data['Year'].unique(), reverse=True))
transmission = st.selectbox("Transmission", options=sorted(data['Transmission'].unique()))
condition = st.selectbox("Condition", options=sorted(data['Condition'].unique()))

# Helper functions
def categorize_price(price_etb):
    lower_bound = (price_etb // 100000) * 100000
    upper_bound = lower_bound + 100000
    return f"{lower_bound:,.0f} - {upper_bound:,.0f} ETB"

def categorize_price_usd(price_usd, step=1000):
    lower_bound = (price_usd // step) * step
    upper_bound = lower_bound + step
    return f"${lower_bound:,.0f} - ${upper_bound:,.0f} USD"

# Persist state for predictions
if "predicted_price_usd" not in st.session_state:
    st.session_state.predicted_price_usd = None
if "predicted_price_etb" not in st.session_state:
    st.session_state.predicted_price_etb = None

# Predict Button
if st.button("Predict Price"):
    # Create a DataFrame from the input
    input_data = pd.DataFrame({
        'Make': [make],
        'Model': [model_name],
        'Fuel': [fuel],
        'Car Age': [2024 - int(year)],  # Calculate Car Age from the selected Year
        'Transmission': [transmission],
        'Condition': [condition]
    })
    
    try:
        # Preprocess the input
        input_processed = preprocessor.transform(input_data)

        # Make the prediction
        st.session_state.predicted_price_etb = model.predict(input_processed)[0]
        st.session_state.predicted_price_usd = st.session_state.predicted_price_etb / etb_to_usd_rate

    except Exception as e:
        st.error(f"Error during prediction: {e}")

# Display results if prediction is made
if st.session_state.predicted_price_usd is not None:
    price_category_etb = categorize_price(st.session_state.predicted_price_etb)
    price_category_usd = categorize_price_usd(st.session_state.predicted_price_usd)
    
    st.write(f"Predicted Price Range: {price_category_etb} ({price_category_usd})")
    st.write(f"Model Accuracy: 93.80%")  # Hardcoded accuracy

    # Custom Exchange Rate Input
    custom_etb_to_usd = st.number_input("Enter a custom exchange rate (ETB per USD):", min_value=0.0, value=etb_to_usd_rate, step=0.1)

    if st.button("Recalculate with Custom Exchange Rate"):
        custom_predicted_price_etb = st.session_state.predicted_price_usd * custom_etb_to_usd
        st.write(f"Price in ETB with custom exchange rate: {custom_predicted_price_etb:,.2f} ETB")
