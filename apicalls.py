import requests
import os
import json

# Specify a URL that resolves to your workspace
URL = "http://127.0.0.1:8000"

# Call each API endpoint and store the responses
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

response1 = requests.post(URL + "/prediction", json={"dataset_path": "testdata.csv"}, headers=headers).text
response2 = requests.get(URL + "/scoring", headers=headers).text
response3 = requests.get(URL + "/summarystats", headers=headers).text
response4 = requests.get(URL + "/diagnostics", headers=headers).text

# combine all API responses
responses = response1 + "\n" + response2 + "\n" + response3 + "\n" + response4  # combine reponses here

# write the responses to your workspace
with open('config.json', 'r') as f:
    config = json.load(f)
model_path = os.path.join(config['output_model_path'])

with open(os.path.join(model_path, "apireturns.txt"), "w") as api_text:
    api_text.write(responses)
