import streamlit as st
import pandas as pd
import pydeck as pdk

# Increase message size limit to 1 GB
# st.set_option("server.maxMessageSize", 1000 * 1024 * 1024)  # 1000 MB

# Load dealer data with column adjustments
def load_dealer_data():
    # Load Makita data
    makita_data = pd.read_csv("makita_dealers.csv")
    makita_data = makita_data.rename(
        columns={
            "Address1": "address",
            "City": "city",
            "State": "state",
            "Zip": "zip",
            "Phone": "phone",
            "Latitude": "lat",
            "Longitude": "lon",
        }
    )
    makita_data["Company"] = "Makita"

    # Load Stanley data
    stanley_data = pd.read_csv("stanley_dealers.csv")
    stanley_data = stanley_data.rename(
        columns={
            "Address": "address",
            "City": "city",
            "State": "state",
            "Postal Code": "zip",
            "Phone": "phone",
            "Latitude": "lat",
            "Longitude": "lon",
        }
    )
    stanley_data["Company"] = "Stanley"

    # Load STIHL data
    stihl_data = pd.read_csv("stihl_dealers_all.csv")
    stihl_data = stihl_data.rename(
        columns={
            "Address": "address",
            "City": "city",
            "State": "state",
            "Postal Code": "zip",
            "Phone": "phone",
            "Latitude": "lat",
            "Longitude": "lon",
        }
    )
    stihl_data["Company"] = "STIHL"

    # Combine all data into a single DataFrame
    combined_data = pd.concat([makita_data, stanley_data, stihl_data], ignore_index=True)

    return combined_data

# Load heatmap data
def load_heatmap_data():
    return pd.read_csv("zipcode_msa_soc_data.csv")

# Filter data based on user input
def filter_heatmap_data(data, selected_title):
    if selected_title:
        data = data[data["OCC_TITLE"] == selected_title]
    return data

def filter_dealer_data(data, selected_companies, selected_state, selected_zip):
    filtered_data = data[data["Company"].isin(selected_companies)]
    
    if selected_state:
        filtered_data = filtered_data[filtered_data["state"] == selected_state]
    if selected_zip:
        filtered_data = filtered_data[filtered_data["zip"].astype(str).str.startswith(str(selected_zip))]

    return filtered_data

# Main Streamlit app
def main():
    # Page configuration
    st.set_page_config(page_title="Dealer Locations & Employment Heatmap", layout="wide")

    # Title
    st.title("Interactive Dealer Locations Map with Employment Heatmap")

    # Load data
    dealer_data = load_dealer_data()
    heatmap_data = load_heatmap_data()

    # Sidebar filters
    st.sidebar.header("Filters")

    # Dealer Filters
    st.sidebar.subheader("Dealer Filters")
    companies = dealer_data["Company"].unique().tolist()
    selected_companies = st.sidebar.multiselect("Select Companies", companies, default=companies)

    states = dealer_data["state"].unique().tolist()
    selected_state = st.sidebar.selectbox("Filter by State", [""] + sorted(states))

    zip_code = st.sidebar.text_input("Filter by ZIP Code (Partial or Full)")

    # Filter dealer data
    filtered_dealer_data = filter_dealer_data(dealer_data, selected_companies, selected_state, zip_code)

    # Heatmap Filters
    st.sidebar.subheader("Heatmap Filters")
    titles = heatmap_data["OCC_TITLE"].unique().tolist()
    selected_title = st.sidebar.selectbox("Filter by Occupation Title", [""] + sorted(titles))

    # Filter heatmap data
    filtered_heatmap_data = filter_heatmap_data(heatmap_data, selected_title)

    # Display data count
    st.write(f"Showing {len(filtered_dealer_data)} dealer locations and {len(filtered_heatmap_data)} heatmap points.")

    # Map settings
    initial_view_state = pdk.ViewState(
        latitude=dealer_data["lat"].mean() if not dealer_data.empty else 37.7749,
        longitude=dealer_data["lon"].mean() if not dealer_data.empty else -122.4194,
        zoom=5,
        pitch=50,
    )

    # Dealer layer
    scatterplot_layer = pdk.Layer(
        "ScatterplotLayer",
        data=filtered_dealer_data,
        get_position="[lon, lat]",
        get_radius=5000,
        get_fill_color="[200, 30, 0, 160]",
        pickable=True,
    )

    # Heatmap layer
    heatmap_layer = pdk.Layer(
        "HeatmapLayer",
        data=filtered_heatmap_data,
        get_position="[Longitude, Latitude]",
        get_weight="TOT_EMP",
        radius_pixels=50,
    )

    # Display map using PyDeck
    st.pydeck_chart(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/streets-v11",
            initial_view_state=initial_view_state,
            layers=[scatterplot_layer, heatmap_layer],
        )
    )

    # Show filtered data in a table
    st.subheader("Dealer Data")
    st.dataframe(filtered_dealer_data)

    st.subheader("Heatmap Data")
    st.dataframe(filtered_heatmap_data)

# Run the app
if __name__ == "__main__":
    main()














# import streamlit as st
# import pandas as pd
# import pydeck as pdk

# # Load dealer data with column adjustments
# def load_data():
#     # Load Makita data
#     makita_data = pd.read_csv("makita_dealers.csv")
#     makita_data = makita_data.rename(
#         columns={
#             "Address1": "address",
#             "City": "city",
#             "State": "state",
#             "Zip": "zip",
#             "Phone": "phone",
#             "Latitude": "lat",
#             "Longitude": "lon",
#         }
#     )
#     makita_data["Company"] = "Makita"

#     # Load Stanley data
#     stanley_data = pd.read_csv("stanley_dealers.csv")
#     stanley_data = stanley_data.rename(
#         columns={
#             "Address": "address",
#             "City": "city",
#             "State": "state",
#             "Postal Code": "zip",
#             "Phone": "phone",
#             "Latitude": "lat",
#             "Longitude": "lon",
#         }
#     )
#     stanley_data["Company"] = "Stanley"

#     # Load STIHL data
#     stihl_data = pd.read_csv("stihl_dealers_all.csv")
#     stihl_data = stihl_data.rename(
#         columns={
#             "Address": "address",
#             "City": "city",
#             "State": "state",
#             "Postal Code": "zip",
#             "Phone": "phone",
#             "Latitude": "lat",
#             "Longitude": "lon",
#         }
#     )
#     stihl_data["Company"] = "STIHL"

#     # Combine all data into a single DataFrame
#     combined_data = pd.concat([makita_data, stanley_data, stihl_data], ignore_index=True)

#     return combined_data

# # Filter data based on user input
# def filter_data(data, selected_companies, selected_state, selected_zip):
#     filtered_data = data[data["Company"].isin(selected_companies)]
    
#     if selected_state:
#         filtered_data = filtered_data[filtered_data["state"] == selected_state]
#     if selected_zip:
#         filtered_data = filtered_data[filtered_data["zip"].astype(str).str.startswith(str(selected_zip))]

#     return filtered_data

# # Main Streamlit app
# def main():
#     # Page configuration
#     st.set_page_config(page_title="Dealer Locations Map", layout="wide")

#     # Title
#     st.title("Interactive Dealer Locations Map")

#     # Load data
#     data = load_data()

#     # Sidebar filters
#     st.sidebar.header("Filters")
#     companies = data["Company"].unique().tolist()
#     selected_companies = st.sidebar.multiselect("Select Companies", companies, default=companies)

#     states = data["state"].unique().tolist()
#     selected_state = st.sidebar.selectbox("Filter by State", [""] + sorted(states))

#     zip_code = st.sidebar.text_input("Filter by ZIP Code (Partial or Full)")

#     # Filter data
#     filtered_data = filter_data(data, selected_companies, selected_state, zip_code)

#     # Display data count
#     st.write(f"Showing {len(filtered_data)} dealer locations.")

#     # PyDeck settings for interactivity
#     initial_view_state = pdk.ViewState(
#         latitude=filtered_data["lat"].mean() if not filtered_data.empty else 37.7749,
#         longitude=filtered_data["lon"].mean() if not filtered_data.empty else -122.4194,
#         zoom=5,
#         pitch=50,
#     )

#     # Dynamic ScatterplotLayer for zoom-responsive radius
#     scatterplot_layer = pdk.Layer(
#         "ScatterplotLayer",
#         data=filtered_data,
#         get_position="[lon, lat]",
#         get_radius="5000 / viewport.zoom ** 0.5",  # Adjust radius based on zoom level
#         get_fill_color="[200, 30, 0, 160]",
#         pickable=True,
#     )


#     # Display map using PyDeck
#     if not filtered_data.empty:
#         st.pydeck_chart(
#             pdk.Deck(
#                 map_style="mapbox://styles/mapbox/streets-v11",
#                 initial_view_state=pdk.ViewState(
#                     latitude=filtered_data["lat"].mean(),
#                     longitude=filtered_data["lon"].mean(),
#                     zoom=5,
#                     pitch=50,
#                 ),
#                 layers=[
#                     pdk.Layer(
#                         "ScatterplotLayer",
#                         data=filtered_data,
#                         get_position="[lon, lat]",
#                         get_radius=5000,
#                         get_fill_color="[200, 30, 0, 160]",
#                         pickable=True,
#                     )
#                 ],
#             )
#         )
#     else:
#         st.write("No data to display on the map.")

#     # Show filtered data in a table
#     st.write("Filtered Data")
#     st.dataframe(filtered_data)

# # Run the app
# if __name__ == "__main__":
#     main()
