# HKTM Vehicle Price Predictor

This repository contains a Streamlit application for predicting vehicle prices in Ethiopian Birr (ETB) and US Dollars (USD). It uses a machine learning model trained on a dataset of vehicle sales.

## Overview

The application allows users to select various car features (Make, Model, Year, Fuel, Transmission, Condition) and then predicts the price range of the vehicle in ETB and USD. The predicted prices are categorized into ranges of 100,000 ETB and $1000 USD for better readability.

## Key Features

- **Dynamic Exchange Rate:** Fetches the latest ETB to USD exchange rate from an external API.
- **Interactive UI:** Uses Streamlit select boxes for easy input of car features.
- **Price Prediction:** Uses a trained machine learning model to predict the vehicle price.
- **Price Categorization:** Groups predicted prices into ranges of 100,000 ETB and $1000 USD.
- **Clear Output:** Displays the exchange rate, predicted price ranges, and model accuracy.

## Repository Structure

hktm-vehicle-price-predictor/
├── app.py # Streamlit application code
├── VehicleData2.csv # Dataset used for training (can be replaced)
├── vehicle_price_model.joblib # Trained machine learning model
├── preprocessor.joblib # Trained preprocessing model
└── README.md # This documentation

## Setup and Usage

### Prerequisites

1.  **Python:** Make sure you have Python 3.7 or higher installed.
2.  **Python Libraries:** Install the required Python libraries by running:

    ```bash
    pip install streamlit pandas joblib numpy requests scikit-learn
    ```

    You might need scikit-learn if it was not installed.

    - Install these in a virtual environment for better management.

### Running the Application Locally

1.  **Clone the Repository:** Clone this GitHub repository to your local machine.
    ```bash
    git clone https://github.com/<your-github-username>/hktm-vehicle-price-predictor.git
    cd hktm-vehicle-price-predictor
    ```
2.  **Run the Streamlit App:** Execute the app:
    ```bash
    streamlit run app.py
    ```
3.  **Open in Browser:** Open the provided URL in your browser to access the application.

## Deployment with Render

Render is a cloud platform that offers free static websites and web services. Here's how you can deploy this Streamlit app using Render:

### 1. Create a Render Account

- Go to [Render](https://render.com/) and sign up for an account.

### 2. Create a New Web Service

- Once logged in, click on **New +** and select **Web Service**.

### 3. Connect to Your GitHub Repository

- Select the **Connect to GitHub** option and connect your `hktm-vehicle-price-predictor` repository to Render.

### 4. Configure Deployment

- **Environment:** Choose `Python 3` environment.
- **Build Command:** Specify the command to install dependencies. This should be:
  ```bash
  pip install -r requirements.txt
  ```
  **Note:** Make sure that you have a file named `requirements.txt` containing the python packages in the root of your repository. To do so, open your terminal, navigate to the root folder of your repository and run the command `pip freeze > requirements.txt`. This will output the list of your packages into that text file.
- **Start Command:** Specify the command to run the Streamlit app. This should be:
  ```bash
  streamlit run app.py
  ```
- **Name** You can use any name you want for your app.
- **Region**: Select your preferred region.
- **Plan**: Select your plan. The free plan works well.

- Click the **Save Changes** or the equivalent button.
- **Deploy**: Click the **Deploy** button on Render and wait for the deployment process to complete.

### 5. Access Your Deployed Application

- After deployment is complete, Render will provide you with a URL to access your application. It will look like `https://<your_app_name>.onrender.com`.

## Disclaimer

- The model used in this application might not be perfectly accurate. The accuracy depends on the quality and size of your training data.
- The exchange rate is fetched from a third-party API and may not always be 100% accurate.
- Make sure to store API keys, passwords, and other secrets outside the repository.

## Author

Your Name Here

## License

[Optional: Add your preferred license, e.g., MIT License]
