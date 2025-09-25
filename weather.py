import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse


load_dotenv()
openweather_api_key =  os.getenv("OPEN_WEATHER_API")

url = 'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={openweather_api_key}'
parsed_url = urlparse(url)
query_params = parse_qs(parsed_url.query)
query_params['appid'] = [openweather_api_key]
city = ''
lat = 0
long = 0
    
def menu_one():
    city = input('Enter your city')
    query_params['q'] = [city]
    new_query = urlencode(query_params, doseq=True)
    new_url = urlunparse(parsed_url._replace(query=new_query))
    try:
        # Make a GET request
        response = requests.get(new_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            count = 1
            print("What State? ")
            for location in data:
                print(f"{count}. State: {location['state']}, Lat: {location['lat']}, Lon: {location['lon']}")
                count+=1
        else:
            print(f"Error: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")

while True:
    print("Menu\nChoose one")
    menu = input("1. Find city \n2. Get Forecast\n" )
    if menu == '1':
        menu_one()
    if menu == '2':
        print("privet")



