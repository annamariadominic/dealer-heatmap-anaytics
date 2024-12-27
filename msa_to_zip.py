import pandas as pd

# Load the filtered census data
census_file = "census/filtered_census_data.xlsx"
census_data = pd.read_excel(census_file)

# Load the ZIP-to-Metro data from the specific sheet
zip_to_metro_file = "census/Zip to Metro Data Excel.xlsx"  # Update with your actual file name
zip_to_metro_data = pd.read_excel(zip_to_metro_file, sheet_name="Zip Code Dataset")

# Filter relevant columns from ZIP-to-Metro data
zip_to_metro_data = zip_to_metro_data[
    ["Zip Code", "Primary CBSA", "Primary CBSA Name", "CBSA Type"]
]

# Ensure Zip Code and Primary CBSA columns are strings
zip_to_metro_data["Zip Code"] = zip_to_metro_data["Zip Code"].apply(lambda x: f"{int(x):05}")
zip_to_metro_data["Primary CBSA"] = zip_to_metro_data["Primary CBSA"].astype(str).str.split('.').str[0]

# Filter relevant columns from census data
census_data = census_data[
    ["AREA", "AREA_TITLE", "AREA_TYPE", "OCC_CODE", "OCC_TITLE", "TOT_EMP"]
]

# Ensure AREA column is string
census_data["AREA"] = census_data["AREA"].astype(str)

# Merge the two datasets based on the MSA code (Primary CBSA and AREA)
merged_data = pd.merge(
    zip_to_metro_data,
    census_data,
    left_on="Primary CBSA",
    right_on="AREA",
    how="inner"
)

# Rename columns for clarity
merged_data.rename(
    columns={
        "Zip Code": "ZIP_CODE",
        "Primary CBSA Name": "MSA_NAME",
        "CBSA Type": "MSA_TYPE",
    },
    inplace=True,
)

# Save the merged data to a CSV file with correct formatting
output_file = "zipcode_msa_soc_data.csv"
merged_data.to_csv(output_file, index=False, quoting=1)  # quoting=1 ensures quotes around text fields

print(f"Data saved to {output_file}")
