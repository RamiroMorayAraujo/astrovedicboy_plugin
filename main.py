# -----------------------
# Initialization Section
# -----------------------
from flask import Flask, request, jsonify
from flask import send_from_directory
from datetime import datetime
from timezonefinder import TimezoneFinder
import pytz
# import sqlite3  # Commented out as we're transitioning to CSV
import requests
import json
import googlemaps
import openai
import time
import nltk
nltk.download('punkt')
import csv  # Already included for CSV handling
import os  # For environment variables
from dotenv import load_dotenv
load_dotenv(dotenv_path='.env')
import re  # Regular expressions library
csv_data = []


PROKERALA_CLIENT_ID = os.getenv("PROKERALA_CLIENT_ID")
PROKERALA_CLIENT_SECRET = os.getenv("PROKERALA_CLIENT_SECRET")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TIMEZONE_API_KEY = os.getenv("TIMEZONE_API_KEY ")

# Initialize Flask app
app = Flask(__name__)

# Initialize an empty list to store tokenized texts
tokenized_texts = []

# Initialize an empty list to store data from the CSV file
csv_data = []

# Read the CSV file into csv_data list (assuming you have a CSV file named 'BEPINS.csv')
with open('BEPINS.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        csv_data.append(row)

# Initialize Google Maps
if os.environ.get('GOOGLE_MAPS_API_KEY'):
    gmaps = googlemaps.Client(key=os.environ.get('GOOGLE_MAPS_API_KEY'))
else:
    gmaps = None
    print("Warning: Google Maps API Key not found. Some features may not work.")



# -----------------------
# Utility Functions
# -----------------------


# -----------------------
# Flask Routes
# -----------------------



# Main function
if __name__ == '__main__':
    csv_data = read_and_tokenize_csv()
    # Get access token from Prokerala API
    token = get_access_token()
    if token:
        print(f"Successfully generated access token: {token}")
        
        # Use Google Maps API to get coordinates for a city (e.g., "New York")
        google_maps_api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
        latitude, longitude = get_coordinates(google_maps_api_key, "New York")
        
        if latitude and longitude:
            # Fetch Rasi Chart using the coordinates
            print(get_rasi_chart(token, str(latitude), str(longitude), "2023-09-21T03:57:48+05:30"))
        else:
            print("Failed to get coordinates.")
    else:
        print("Failed to generate access token.")
        
   # app.run(debug=True, port=5001)


    sample_rasi_chart = "Aries"  # Replace with a sample Rasi chart data
    result = initial_filtering(sample_rasi_chart)
    print("Initial Filtering Result:", result)

