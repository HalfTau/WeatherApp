import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

load_dotenv()
openweather_api_key =  os.getenv("OPEN_WEATHER_API")

#googled and taken from microsoft AI
def clear_screen():
    # For Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # For macOS and Linux
    else:
        _ = os.system('clear')

def build_geo_url(city): 
    return f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={openweather_api_key}"

def build_weather_url(lat, lon, units):
    return f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={openweather_api_key}&units={units}"

#collect the user's city 
def menu_one():
    clear_screen()
    city = input('Enter your city: ')
    geo_url = build_geo_url(city)

    try:
        # Make a GET request
        response = requests.get(geo_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            if len(data) > 1:
                for i, location in enumerate(data, start=1):
                    state = location.get('state', 'N/A')
                    print(f"{i}. {location['name']}, {state}, Lat: {location['lat']}, Lon: {location['lon']}")
                choice = int(input(f"There are multiple matches for {city}. Choose one: "))
                real_location = data[choice - 1]
            else:
                real_location = data[0]           
            return real_location


        else:
            print(f"Error: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")


def menu_two(loc):
    weather_url = build_weather_url(loc['lat'], loc['lon'], "imperial")
    try:
        # Make a GET request
        response = requests.get(weather_url)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            #extracting information
            return {
                "state": loc.get("state", "Unknown"),
                "city": data.get("name", "Unknown"),
                "country": data["sys"].get("country", "Unknown"),
                "temperature_f": round(data["main"]["temp"]),
                "feels_like_f": round(data["main"]["feels_like"]),
                "humidity": data["main"].get("humidity"),
                "description": data["weather"][0].get("description", "No description")
            }

            #return(temperature_convert)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")

loc = None
#main menu loop
while True:
    print("Menu\nChoose one")
    menu = input("1. Find city \n2. Get Forecast\n" )
    if menu == '1':
        clear_screen()
        loc = menu_one()     
    if menu == '2':
        clear_screen()
        if loc:
            results = menu_two(loc)
            #print(f"current weather for {results['city']}")
            print(f"Weather for: {results['city']}, {results['state']}")
            print(f"temp: {results['temperature_f']} \ndescription: {results['description']}")
        else: 
            print("oops! enter a city first.")

    



