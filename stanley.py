import requests
import csv

# API endpoint and parameters
url = "https://api.sbdinc.com/SBDLocationService/v1/api/Locations/allRetailers"
params = {
    "Type": "R",
    "BrandName": "stanley",
    "MarketCode": "US",
    "Categories": "",
    "page": 1,
    "ItemsPerPage": 100
}

# Headers with subscription key
headers = {
    "agora-subscription-key": "21fee0ece7d2447f82288e7a55aa38c6"
}

# Prepare list to hold all dealer data
all_dealers = []

# Pagination loop
while True:
    print(f"Fetching page {params['page']}...")
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"API Response for Page {params['page']} received.")  # Debugging
        
        # Extract the dealer data from the 'items' key
        dealers = data.get("items", [])  # Adjusted to fetch data from the 'items' key
        
        if not dealers:  # If no more data, break the loop
            break
        
        for dealer in dealers:
            coordinates = dealer.get("coordinates", "").split(", ")
            lat, lon = (float(coordinates[0]), float(coordinates[1])) if len(coordinates) == 2 else (None, None)
            all_dealers.append({
                "Name": dealer.get("poi", "N/A"),
                "Address": dealer.get("address1", "N/A"),
                "City": dealer.get("city", "N/A"),
                "State": dealer.get("state", "N/A"),
                "Postal Code": dealer.get("postalCode", "N/A"),
                "Latitude": lat,
                "Longitude": lon,
                "Phone": dealer.get("phone", "N/A"),
            })
        
        # Go to the next page
        params["page"] += 1
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}, Message: {response.text}")
        break

# Verify if any dealers were extracted
if not all_dealers:
    print("No dealers were extracted. Please check the API response and key names.")
else:
    # Save all dealers to a CSV file
    csv_file = "stanley_dealers.csv"
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["Name", "Address", "City", "State", "Postal Code", "Latitude", "Longitude", "Phone"])
        writer.writeheader()
        writer.writerows(all_dealers)
    
    print(f"Dealer data saved to {csv_file}")
