import folium
import pandas as pd

# Load the data from CSV
data = pd.read_csv('stihl_dealers.csv')

# Create a base map centered around the average latitude and longitude
avg_lat = data['Latitude'].mean()
avg_lon = data['Longitude'].mean()
m = folium.Map(location=[avg_lat, avg_lon], zoom_start=10)

# Add markers for each dealer
for _, row in data.iterrows():
    popup_text = (
        f"<b>{row['Name']}</b><br>"
        f"Address: {row['Address']}, {row['City']}, {row['State']} {row['Postal Code']}<br>"
        f"Phone: {row['Phone']}<br>"
        f"Today’s Hours: {row['Today’s Hours']}"
    )
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=popup_text,
    ).add_to(m)

# Save the map to an HTML file
m.save('dealers_map.html')

print("Map has been saved to 'dealers_map.html'. Open this file in a browser to view the map.")
