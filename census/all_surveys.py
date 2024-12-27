import requests
import json

# BLS API URL to retrieve all surveys
url = "https://api.bls.gov/publicAPI/v2/surveys"

output_file = "bls_surveys.json"  # Output file name

try:
    # Send a GET request to retrieve all surveys
    response = requests.get(url)
    
    # Debug: Print the response status code
    print(f"Response Status Code: {response.status_code}")
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response JSON
        data = response.json()
        
        # Save to a file
        with open(output_file, "w") as file:
            json.dump(data, file, indent=4)
        
        print(f"Survey data saved to: {output_file}")
        
        # Optional: Print available surveys to console
        if "Surveys" in data:
            print("\nAvailable Surveys:")
            for survey in data["Surveys"]:
                print(f"ID: {survey['survey_abbreviation']}, Name: {survey['survey_name']}")
        else:
            print("No surveys found in the response.")
    else:
        print(f"Failed to retrieve surveys. HTTP Status Code: {response.status_code}")
        print(response.text)

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
