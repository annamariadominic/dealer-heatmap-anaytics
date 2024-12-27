import requests
import json

# BLS API URL for multiple series IDs
url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"

# List of series IDs (replace with your desired series IDs)
series_ids = [
    "OEUM001018000000011202101",
    "OEUM001018000000011202102",
    "OEUM001018000000011202103"  # Add more series IDs as needed
]

API_KEY = "30d33b109a75458791f024d1b3e2ae6c"  # Replace with your API key

# API Payload
payload = {
    "seriesid": series_ids,
    "startyear": "2020",  # Adjust as needed
    "endyear": "2023",
    "registrationkey": API_KEY
}

# API Headers
headers = {
    "Content-Type": "application/json"
}

# Send the POST request
try:
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # Print the raw JSON response as is
    print(response.text)

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")