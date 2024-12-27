import requests
import csv
import os

# Paths
zip_file = os.path.join("zipcodes", "uszips.csv")  # Path to your ZIP code CSV file
output_file = "makita_dealers.csv"

# API endpoint
url = "https://www.makitatools.com/api/getretailersbyretailertypewithinmiles"

# Headers
headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Content-Type": "application/json"
}

# Set to store unique dealer names
unique_dealers = set()

# Open the CSV file for writing
with open(zip_file, newline='', encoding='utf-8') as zip_file, open(output_file, mode='w', newline='', encoding='utf-8') as output_csv:
    reader = csv.DictReader(zip_file)
    writer = csv.writer(output_csv)
    
    # Write the header row for the output CSV
    writer.writerow(['Name', 'Address1', 'Address2', 'City', 'State', 'Zip', 'Phone', 'Latitude', 'Longitude', 'ToolType', 'Distance', 'URL'])

    # Process each ZIP code from the input file
    for row in reader:
        zipcode = row['zip']
        latitude = float(row['lat'])
        longitude = float(row['lng'])
        
        print(f"Fetching dealers for ZIP code: {zipcode}...")
        
        # Parameters for the GET request
        params = {
            "zip": zipcode,
            "lat": latitude,
            "lon": longitude,
            "miles": 50,  # Radius in miles
            "retailerType": 65535,
            "shopEventId": "",
            "_": 1734377074131  # Arbitrary timestamp
        }
        
        # Send the GET request
        response = requests.get(url, params=params, headers=headers)
        
        if response.status_code == 200:
            dealers = response.json()
            
            # Process each dealer in the response
            for dealer in dealers:
                dealer_name = dealer['Name']
                
                # Avoid duplicates using the unique_dealers set
                if dealer_name not in unique_dealers:
                    unique_dealers.add(dealer_name)
                    
                    writer.writerow([
                        dealer['Name'],
                        dealer.get('Address1', ''),
                        dealer.get('Address2', ''),
                        dealer.get('City', ''),
                        dealer.get('State', ''),
                        dealer.get('Zip', ''),
                        dealer.get('Phone', 'N/A'),
                        dealer.get('Latitude', ''),
                        dealer.get('Longitude', ''),
                        dealer.get('ToolType', ''),
                        dealer.get('Distance', ''),
                        dealer.get('URL', '')
                    ])
        else:
            print(f"Failed to fetch data for ZIP code {zipcode}. Status code: {response.status_code}, Message: {response.text}")

print(f"Dealer data saved to {output_file}")
