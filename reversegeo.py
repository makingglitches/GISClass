import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time

# Function to reverse geocode coordinates
def reverse_geocode(latitude, longitude, geolocator):
    try:
        co = f"{latitude}, {longitude}"
        location = geolocator.reverse(co, exactly_one=True, language='en')
        
        if location is None:
            print("location is null")

        return None if location is None else location.address
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        return f"Error: Geocode failed with error {type(e).__name__}"

# Replace 'your_input_file.csv' with your CSV file name
input_file = '/home/john/Documents/HACC Notes/Introduction To Geospatial Technology/Week 5/installations_mil.csv'

# Replace 'x' and 'y' with your column names for latitude and longitude
latitude_column = 'y'
longitude_column = 'x'

# Read CSV into a pandas DataFrame
try:
    df = pd.read_csv(input_file)
except FileNotFoundError:
    print(f"Error: File '{input_file}' not found.")
    exit(1)
except pd.errors.EmptyDataError:
    print(f"Error: File '{input_file}' is empty.")
    exit(1)

# Initialize geolocator with custom user agent
geolocator = Nominatim(user_agent="lokisgeo")

# Create lists to store results
coordinates = []
addresses = []

# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    latitude = row[latitude_column]
    longitude = row[longitude_column]

    # Introduce a delay of 1 second before each geocoding request
    time.sleep(1)

    # Perform reverse geocoding
    address = reverse_geocode(latitude, longitude, geolocator)
    
    # Append coordinates and addresses to lists
    coordinates.append((latitude, longitude))
    addresses.append(address)

# Add new columns for coordinates and addresses to the original DataFrame
df['Coordinates'] = coordinates
df['Address'] = addresses

# Define output CSV file name
output_file = 'output_with_addresses.csv'

# Write the updated DataFrame to a new CSV file
df.to_csv(output_file, index=False)


print(f"Output saved to '{output_file}'.")

