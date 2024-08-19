import pandas as pd

# Load the GeoJSON files for different years from a directory
geojson_directory = 'geojson3'


properties_df = pd.read_csv("datasets/flood_risk_final.csv")
portfolio_data = pd.read_csv('datasets/chicago_properties4.csv')
map_data = pd.read_csv('datasets/properties_df.csv')

# Set pandas display options to show full precision
pd.set_option('display.float_format', lambda x: f'{x:.15g}')
chicago_properties = pd.read_csv('datasets/chicago_properties4.csv')