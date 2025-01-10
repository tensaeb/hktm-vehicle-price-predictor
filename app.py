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
    # st.success("Model and Preprocessor Loaded Successfully!") # Not necessary
except FileNotFoundError:
    st.error("Error: Model or preprocessor file not found. Please make sure the files 'vehicle_price_model.joblib' and 'preprocessor.joblib' are in the same directory as this script or they are on Google Colab")
    st.stop()
except Exception as e:
    st.error(f"Error loading model or preprocessor: {e}")
    st.stop()


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


# Load data to get unique values for dropdowns
data = pd.read_csv('VehicleData2.csv')
data.dropna(subset=[' Price '], inplace=True)  # Ensure no NaN in target column
data.fillna('Unknown', inplace=True)  # Fill NaN values in other columns

# Fetch the Exchange rate once
etb_to_usd_rate = get_exchange_rate()

if etb_to_usd_rate is None:
        st.error("Could not retrieve the current exchange rate. Please check your internet connection.")
        st.stop()

# UI Elements
st.title("HKTM Vehicle Price Predictor")
st.markdown("Select the car features to predict the price.")
st.write(f"Today's Exchange Rate: 1USD = {etb_to_usd_rate:.2f} ETB")  # Display exchange rate on top


# Dropdown for Make
make = st.selectbox("Make", options=sorted(data['Make'].unique()))

# Dynamically update Model options based on selected Make
filtered_data = data[data['Make'] == make]
filtered_models = filtered_data['Model'].unique()
model_name = st.selectbox("Model", options=sorted(filtered_models))

# Dynamically update Fuel options based on selected Make and Model
filtered_fuels = filtered_data[filtered_data['Model'] == model_name]['Fuel'].unique()
fuel = st.selectbox("Fuel", options=sorted(filtered_fuels))

# Non-dynamic dropdowns for Year, Transmission, and Condition
year = st.selectbox("Year", options=sorted(data['Year'].unique(), reverse=True))
transmission = st.selectbox("Transmission", options=sorted(data['Transmission'].unique()))
condition = st.selectbox("Condition", options=sorted(data['Condition'].unique()))


def categorize_price(price_etb):
    """Categorizes the price into ranges of 100,000 ETB."""
    lower_bound = (price_etb // 100000) * 100000
    upper_bound = lower_bound + 100000
    return f"{lower_bound:,.0f} - {upper_bound:,.0f} ETB"

def categorize_price_usd(price_usd, step = 1000): #Added an optional step value if we want to vary
    """Categorizes the price into ranges of $1000."""
    lower_bound = (price_usd // step) * step
    upper_bound = lower_bound + step
    return f"${lower_bound:,.0f} - ${upper_bound:,.0f} USD"

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
     # Preprocess the input
    try:
        input_processed = preprocessor.transform(input_data)
    except Exception as e:
          st.error(f"Error during preprocessing {e}")


    # Make the prediction
    try:
        predicted_price_etb = model.predict(input_processed)[0]
        predicted_price_usd = predicted_price_etb / etb_to_usd_rate

         # Categorize the predicted price
        price_category_etb = categorize_price(predicted_price_etb)
        price_category_usd = categorize_price_usd(predicted_price_usd)

        # Display the prediction
        st.write(f"Predicted Price Range: {price_category_etb}  ({price_category_usd})")
        # Use model accuracy
        st.write(f"Model Accuracy: 93.80%")  # Hardcoded

    except Exception as e:
        st.error(f"Error during prediction: {e}")