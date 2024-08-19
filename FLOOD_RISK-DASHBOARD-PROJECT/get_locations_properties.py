import pandas as pd
import requests
import json

nominatim_geocoding_url = 'https://nominatim.openstreetmap.org/search'



try:
    with open('flood_data/geocode_cache.json', 'r') as f:
        geocode_cache = json.load(f)
except FileNotFoundError:
    geocode_cache = {}

def get_location_by_zip(zip_code):
    if zip_code in geocode_cache:
        print(f"Using cached geocode for ZIP Code {zip_code}")
        return tuple(geocode_cache[zip_code])  # Convert list back to tuple
    
    try:
        params = {
            'q': zip_code,
            'format': 'json',
            'countrycodes': 'us'
        }
        response = requests.get(nominatim_geocoding_url, params=params, timeout=10)
        results = response.json()

        if results:
            location = results[0]
            lat, lon = float(location['lat']), float(location['lon'])
            geocode_cache[zip_code] = [lat, lon]  
            return lat, lon
        else:
            return None, None
    except Exception as e:
        print(f"Error occurred: {e}")
        return None, None


def get_lat_long(properties_df):
    # Get latitude and longitude for each ZIP Code
    lat_long_list = []
    for z in properties_df['ZIP Code']:
        lat_long = get_location_by_zip(z)
        if lat_long != (None, None):
            lat_long_list.append(lat_long)
        else:
            lat_long_list.append((float('nan'), float('nan')))

    # print(lat_long_list)

    # Create a DataFrame from the lat_long_list
    lat_long_df = pd.DataFrame(lat_long_list, columns=['latitude', 'longitude'])
    # print(lat_long_df)

    # Merge this DataFrame with the original properties_df
    # Drop existing 'latitude' and 'longitude' columns if they exist
    properties_df = properties_df.loc[:,~properties_df.columns.duplicated()]  # Remove duplicate columns first if any
    # print(properties_df)

    for column in ['latitude', 'longitude']:
        if column in properties_df.columns:
            properties_df = properties_df.drop(columns=[column], errors='ignore')

    properties_df = pd.concat([properties_df.reset_index(drop=True), lat_long_df], axis=1)

    return properties_df
    # Check the DataFrame after geocoding
    # print("Properties DataFrame after geocoding:")
    # print(properties_df)
