import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse


load_dotenv()
openweather_api_key =  os.getenv("OPEN_WEATHER_API")

geo_url = 'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={openweather_api_key}'
geo_parsed_url = urlparse(geo_url)
geo_query_params = parse_qs(geo_parsed_url.query)
geo_query_params['appid'] = [openweather_api_key]

weather_url = 'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}'
weather_parsed_url = urlparse(weather_url)
weather_query_params = parse_qs(weather_parsed_url.query)
weather_query_params['appid'] = [openweather_api_key]

#googled and taken from microsoft AI
def clear_screen():
    # For Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # For macOS and Linux
    else:
        _ = os.system('clear')

def k_convert(temp):
    return temp * 1.8 - 459.67

def menu_two(loc):
    print(f"here we are: {loc}")
    weather_query_params['lat'] = loc['lat']
    weather_query_params['lon'] = loc['lon']
    new_query = urlencode(weather_query_params, doseq=True)
    new_url = urlunparse(weather_parsed_url._replace(query=new_query))
    try:
        # Make a GET request
        response = requests.get(new_url)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            #extracting information
            city = data["name"]
            country = data["sys"]["country"]
            weather_main = data["weather"][0]["main"]
            weather_description = data["weather"][0]["description"]
            temperature = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            temperature_convert = k_convert(temperature)
            return(temperature_convert)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")

#collect the user's city 
def menu_one():
    clear_screen()
    city = input('Enter your city')
    #put entered city into API URL
    geo_query_params['q'] = [city]
    new_query = urlencode(geo_query_params, doseq=True)
    new_url = urlunparse(geo_parsed_url._replace(query=new_query))

    try:
        # Make a GET request
        response = requests.get(new_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            count = 0

            for location in data:
                print(f"{count+1}. {location['name']}, {location['state']}, Lat: {location['lat']}, Lon: {location['lon']}")
                count+=1
            state = int(input("what state? "))
            real_location = data[state - 1]

            return(real_location)


        else:
            print(f"Error: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")



loc = []
#main menu loop
while True:
    
    print("Menu\nChoose one")
    menu = input("1. Find city \n2. Get Forecast\n" )
    if menu == '1':
        loc = menu_one()
        print(loc['lat'])
    if menu == '2':
        print(menu_two(loc))




