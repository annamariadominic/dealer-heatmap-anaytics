import requests
import csv
import os

# Paths
zip_file = os.path.join("zipcodes", "uszips.csv")  # Path to your ZIP code CSV file
output_file = "stihl_dealers_all.csv"

# API endpoint and headers
url = "https://www.stihlusa.com/api/dealers/"
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://www.stihlusa.com",
    "Referer": "https://www.stihlusa.com/locator",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

# Set to store unique dealer IDs
unique_dealers = set()

# Read ZIP codes and iterate over them
with open(zip_file, newline='', encoding='utf-8') as zip_file, open(output_file, mode='w', newline='', encoding='utf-8') as output_csv:
    reader = csv.DictReader(zip_file)
    writer = csv.writer(output_csv)
    
    # Write the header row for the output CSV
    writer.writerow(['ID', 'Name', 'Address', 'City', 'State', 'Postal Code', 'Latitude', 'Longitude', 'Phone', 'Today’s Hours'])
    
    # Process each ZIP code from the input file
    for row in reader:
        zipcode = row['zip']
        latitude = float(row['lat'])
        longitude = float(row['lng'])
        
        print(f"Fetching dealers for ZIP code: {zipcode}...")
        
        # Payload for the API request
        payload = {
            "locatorId": "pcl-000000",
            "query": {
                "term": "",
                "filters": [],
                "googleGeocodingResult": {
                    "status": "OK",
                    "results": [
                        {
                            "formatted_address": f"{zipcode}, USA",
                            "geometry": {
                                "location": {
                                    "lat": latitude,
                                    "lng": longitude
                                }
                            }
                        }
                    ]
                },
                "coordinates": {
                    "latitude": latitude,
                    "longitude": longitude
                }
            },
            "paging": {
                "skip": 0,
                "take": 50  # Number of results per request
            }
        }

        # Handle pagination
        while True:
            response = requests.post(url, json=payload, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                dealers = data.get('data', {}).get('results', [])
                
                if not dealers:
                    break  # No more dealers for this ZIP code
                
                # Write each dealer to the output CSV
                for dealer in dealers:
                    dealer_id = dealer['id']
                    
                    # Avoid duplicates using the unique_dealers set
                    if dealer_id not in unique_dealers:
                        unique_dealers.add(dealer_id)
                        address = dealer['address']
                        
                        writer.writerow([
                            dealer_id,
                            dealer['name'],
                            address['address1'],
                            address['city'],
                            address['state'],
                            address['postalCode'],
                            address['latitude'],
                            address['longitude'],
                            dealer.get('phone', 'N/A'),
                            dealer.get('storeHours', {}).get('today', 'N/A')
                        ])
                
                # Move to the next page
                payload['paging']['skip'] += payload['paging']['take']
            else:
                print(f"Failed to fetch dealers for ZIP code {zipcode}. Status code: {response.status_code}, Message: {response.text}")
                break

print(f"Dealer data saved to {output_file}")
