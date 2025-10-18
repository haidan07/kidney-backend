from flask import Flask, request
import requests

app = Flask(__name__)

DEPLOYMENT_URL = "https://au-syd.ml.cloud.ibm.com/ml/v4/deployments/a72ecc70-9a1e-4d5f-b4f7-4893d83e6c12/predictions?version=2021-05-01"
API_KEY = "ApiKey-af6e77e3-6c28-4cb8-a0fd-062720237944"

def get_access_token():
    token_url = "https://iam.cloud.ibm.com/identity/token"
    data = {
        "apikey": API_KEY,
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey"
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(token_url, data=data, headers=headers)
    return response.json()["access_token"]

def get_prediction(values):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {get_access_token()}"
    }
    payload = {
        "input_data": [{
            "fields": ["gravity", "urea", "ph", "osmolality", "conductivity", "calcium"],
            "values": [values]
        }]
    }
    response = requests.post(DEPLOYMENT_URL, headers=headers, json=payload)
    return response.json()["predictions"][0]["values"][0][0]

@app.route('/predict', methods=['POST'])
def predict():
    data = request.form
   values = [
  float(data['gravity']),
  float(data['urea']),
  float(data['ph']),
  float(data['osmolality']),
  float(data['conductivity']),
  float(data['calcium'])
]

    result = get_prediction(values)
    diagnosis = "You have kidney stone" if result == 1 else "You don't have kidney stone"
    return diagnosis
